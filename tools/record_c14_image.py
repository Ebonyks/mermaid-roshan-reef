"""Preserve an actual built-in image result and its exact submitted arguments."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'assets_src/cinematics/d1_c14_castle_team_cleanup_v1'


def sha(path):
	with path.open('rb') as handle:
		return hashlib.file_digest(handle, 'sha256').hexdigest()


def record(job_path, native, output, attempt, note):
	job = json.loads(job_path.read_text(encoding='utf-8-sig'))
	assert 'referenced_image_paths' in job and not job.get('num_last_images_to_include')
	assert 1 <= len(job['referenced_image_paths']) <= 5
	target = (PACKET / output).resolve()
	target.relative_to(PACKET.resolve())
	assert target.suffix.lower() == '.png'
	target.parent.mkdir(parents=True, exist_ok=True)
	if target.exists():
		assert sha(target) == sha(native), 'Do not overwrite a different candidate'
	else:
		shutil.copyfile(native, target)
	inputs = []
	for name in job['referenced_image_paths']:
		path = Path(name)
		with Image.open(path) as picture:
			inputs.append({'path': name, 'sha256': sha(path), 'dimensions': list(picture.size)})
	with Image.open(target) as picture:
		dimensions = list(picture.size)
	data = {'schema':'c14-builtin-image-record-v1', 'output_path':output,
		'output_sha256':sha(target), 'dimensions':dimensions,
		'native_output_path':native.as_posix(), 'native_output_sha256':sha(native),
		'prompt':job['prompt'], 'prompt_sha256':hashlib.sha256(job['prompt'].encode()).hexdigest(),
		'referenced_image_paths':job['referenced_image_paths'], 'input_images':inputs,
		'attempt':attempt, 'generation_method':'builtin_image_gen', 'human_decision':'pending',
		'used_as_delivery_pixels':False, 'delivery_accepted':False, 'review_note':note}
	path = PACKET / 'generation_records' / (target.stem + '.json')
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
	print(json.dumps({'path':output,'sha256':data['output_sha256'],'dimensions':dimensions}))


if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('--job',type=Path,required=True)
	parser.add_argument('--native',type=Path,required=True)
	parser.add_argument('--output',required=True)
	parser.add_argument('--attempt',type=int,default=1)
	parser.add_argument('--note',default='Human approval pending; no delivery acceptance.')
	args=parser.parse_args()
	record(args.job,args.native,args.output,args.attempt,args.note)
