"""Expose authored plant regions in stage ORAs without resampling seams."""
from pathlib import Path
import hashlib
import io
import zipfile
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

P = Path(__file__).resolve().parent
SOURCES = {
    'bellflower_breeze.png': 'bellflower/bellflower-editable.ora',
    'huckleberry_breeze.png': 'huckleberry/huckleberry-editable.ora',
    'conifer_breeze.png': 'conifer/conifer-editable.ora',
    'arrival_boughs.png': 'arrival_boughs/arrival-boughs-editable.ora',
}

def separate(canvas, source, inverse, cell_size, prefix, evidence):
    relative = SOURCES.get(Path(source).name)
    if relative is None:
        box = canvas.getbbox()
        return [(prefix, canvas.crop(box), box[:2], source)]
    path = P / relative
    names = []
    labels = np.zeros((cell_size[1], cell_size[0]), dtype='uint8')
    covered = np.zeros_like(labels, dtype=bool)
    with zipfile.ZipFile(path) as archive:
        tree = ET.fromstring(archive.read('stack.xml'))
        assert (int(tree.attrib['w']), int(tree.attrib['h'])) == cell_size
        for row in reversed(list(tree.find('stack'))):
            name = row.attrib['name']
            if name == 'fixed_background_and_concealed_fill':
                continue  # This is already owned by the stage background tile.
            image = Image.new('RGBA', cell_size)
            part = Image.open(io.BytesIO(archive.read(row.attrib['src']))).convert('RGBA')
            image.alpha_composite(part, (int(row.attrib.get('x', 0)), int(row.attrib.get('y', 0))))
            visible = np.array(image)[:, :, 3] > 0
            labels[visible] = len(names)
            covered |= visible
            names.append(name)
    # Give resampled fringe pixels to their nearest actual component, rather
    # than scattering detached edge flecks into the default stem layer.
    nearest = distance_transform_edt(~covered, return_distances=False, return_indices=True)
    labels = labels[tuple(nearest)]
    # Transform categorical ownership once. Partition the already-rendered
    # card pixels, avoiding independently filtered masks that open seams.
    world_labels = np.array(Image.fromarray(labels).transform(canvas.size, Image.Transform.AFFINE, inverse, Image.Resampling.NEAREST))
    alpha = np.array(canvas)[:, :, 3]
    result = []
    for index, name in enumerate(names):
        image = canvas.copy()
        image.putalpha(Image.fromarray(np.where(world_labels == index, alpha, 0).astype('uint8')))
        box = image.getbbox()
        if box:
            result.append((prefix + ' / ' + name, image.crop(box), box[:2], source))
    evidence[relative] = {
        'source': path.relative_to(P.parents[2]).as_posix(),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'components': names,
        'method': 'authored source-region ownership applied to rendered card; no new artwork or hidden geometry',
    }
    return result
