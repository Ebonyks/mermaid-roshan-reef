from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
from scipy import ndimage as ndi
import json,hashlib,re,sys
sys.path.insert(0, str(Path("tmp/opera-mask-deps").resolve()))
import cv2
src=Path('assets_src/concepts/opera_four_floors_2026-09-06');out=Path('assets/flats/castle/opera_house_four_floors'); fg=out/'foreground';fg.mkdir(exist_ok=True)
original=Image.open(src/'venue_native_v7.png').convert('RGBA'); clean=Image.open(src/'venue_clean_v7.png').convert('RGBA')
# Hand-traced source-space silhouettes. Lounge rugs belong to their furniture group.
polygons={
'flower_stand':[(0,550),(15,545),(23,538),(34,537),(43,543),(47,531),(57,526),(66,533),(67,541),(91,547),(115,558),(128,576),(130,594),(122,600),(122,644),(142,638),(158,650),(159,664),(153,673),(165,685),(160,710),(158,732),(143,744),(108,753),(64,759),(0,754)],
'snack_stand':[(0,700),(10,702),(13,695),(23,700),(27,723),(42,722),(53,718),(65,722),(74,735),(72,746),(95,762),(98,779),(112,771),(113,754),(122,756),(130,779),(139,775),(138,751),(152,762),(158,774),(160,745),(173,757),(181,748),(197,739),(190,762),(207,754),(200,779),(212,781),(200,796),(211,803),(201,820),(207,837),(204,854),(193,867),(174,873),(163,868),(151,882),(144,901),(118,911),(82,920),(43,928),(41,936),(25,938),(15,931),(9,912),(0,909)],
'left_couch':[(208,781),(223,767),(238,762),(239,753),(248,746),(263,747),(264,727),(271,721),(280,722),(282,729),(305,718),(348,709),(353,699),(365,688),(376,698),(386,715),(422,720),(446,732),(446,720),(452,718),(458,724),(457,749),(462,761),(462,770),(487,778),(504,793),(506,810),(490,829),(459,842),(416,850),(365,855),(309,849),(264,838),(228,823),(211,806)],
'planter':[(740,808),(748,793),(775,780),(778,759),(789,748),(796,742),(796,735),(784,729),(801,729),(792,716),(810,721),(813,704),(824,716),(833,699),(840,716),(853,708),(850,722),(870,715),(857,734),(870,734),(884,747),(890,773),(891,784),(915,795),(928,814),(928,836),(920,853),(911,869),(900,871),(895,862),(874,868),(873,878),(858,884),(846,879),(842,871),(783,865),(767,872),(752,866),(749,852),(739,837)],
'right_couch':[(1165,780),(1190,766),(1211,765),(1211,752),(1220,746),(1212,731),(1214,723),(1223,720),(1228,728),(1265,715),(1285,713),(1287,703),(1296,691),(1305,691),(1314,707),(1330,715),(1371,726),(1398,744),(1406,750),(1411,766),(1432,776),(1450,790),(1456,806),(1447,821),(1424,839),(1381,850),(1323,855),(1267,848),(1215,839),(1180,823),(1164,805)],
'drinks_cart':[(1480,695),(1494,684),(1496,661),(1500,647),(1519,634),(1537,637),(1547,645),(1547,621),(1537,605),(1539,578),(1551,560),(1550,549),(1563,549),(1570,558),(1585,549),(1599,548),(1608,558),(1622,567),(1640,585),(1645,609),(1637,632),(1621,648),(1610,650),(1614,662),(1628,649),(1638,653),(1637,642),(1648,651),(1668,635),(1672,635),(1672,779),(1654,783),(1635,773),(1619,780),(1611,797),(1590,808),(1572,801),(1561,799),(1534,792),(1514,786),(1499,788),(1485,780),(1481,768),(1486,750),(1484,725)]}
manifest={'method':'owner_authorized_deterministic_alpha_masking','source':'venue_native_v7.png','source_sha256':hashlib.sha256((src/'venue_native_v7.png').read_bytes()).hexdigest(),'rgb_pixels_modified':False,'objects':{}}
recomposite=clean.copy()
for name,points in polygons.items():
 mask=Image.new('L',original.size);ImageDraw.Draw(mask).polygon(points,fill=255)
 # Feather only alpha by subpixel coverage; RGB remains byte-identical to source.
 bounds=mask.getbbox(); rgba=original.copy();rgba.putalpha(mask);card=rgba.crop(bounds);card.save(fg/(name+'.png'));recomposite.alpha_composite(rgba)
 rect=[bounds[0]*1280/1672,bounds[1]*720/941,(bounds[2]-bounds[0])*1280/1672,(bounds[3]-bounds[1])*720/941]
 manifest['objects'][name]={'native_bounds':list(bounds),'canvas_rect':rect,'polygon':points,'sha256':hashlib.sha256((fg/(name+'.png')).read_bytes()).hexdigest()}
 # Runtime uses exact native position and dimensions, avoiding art redesign/scale drift.
 p=Path('scripts/opera_venue_foreground.gd');s=p.read_text();s=re.sub(r'("art": "'+name+r'", "rect": )Rect2\([^)]*\)',lambda m:m[1]+'Rect2('+', '.join(f'{v:.5f}' for v in rect)+')',s);p.write_text(s)
(src/'foreground_masks.json').write_text(json.dumps(manifest,indent=2)+'\n')
recomposite.convert('RGB').save('tmp/opera-foreground-recomposite.png')
for i in range(2):clean.crop((i*836,0,(i+1)*836,941)).convert('RGB').save(out/f'venue_{i}.png')
# Explicit source-coordinate contours retain dark ink and the entire stems/cakes.
contours={
'flower':[(142,123),(167,111),(193,99),(220,99),(246,111),(253,94),(277,72),(302,63),(322,60),(338,71),(357,102),(368,133),(371,155),(365,171),(390,165),(417,180),(433,201),(454,215),(455,231),(441,251),(421,273),(392,282),(369,279),(383,302),(396,341),(384,368),(364,372),(337,360),(311,343),(290,326),(282,305),(279,344),(290,380),(312,419),(351,452),(394,465),(406,479),(403,491),(389,498),(368,496),(338,484),(307,465),(284,444),(263,461),(234,470),(204,466),(180,452),(160,428),(145,399),(131,376),(117,359),(119,348),(144,344),(170,347),(204,357),(231,373),(251,396),(268,418),(257,378),(256,340),(261,309),(244,317),(218,335),(187,339),(168,331),(151,315),(154,284),(174,256),(194,238),(207,231),(181,226),(158,213),(143,194),(135,168),(133,144),(135,130)],
'petal':[(666,409),(682,390),(690,365),(694,329),(700,292),(714,254),(735,231),(766,216),(797,200),(817,198),(837,216),(858,243),(878,276),(884,306),(876,337),(860,361),(836,381),(802,399),(763,416),(725,430),(699,433),(678,430),(665,423)],
'cup_empty':[(272,602),(315,604),(355,611),(380,622),(393,640),(405,676),(423,718),(435,763),(440,802),(433,841),(416,873),(391,900),(366,914),(374,927),(366,939),(339,947),(292,951),(244,947),(207,938),(189,927),(186,915),(192,904),(171,891),(148,873),(131,849),(120,819),(115,788),(118,751),(129,705),(144,669),(154,641),(166,626),(189,615),(225,606)],
'cup_full':[(769,598),(807,601),(849,610),(875,623),(887,642),(900,678),(917,721),(926,767),(927,807),(918,845),(899,878),(878,898),(860,911),(869,924),(861,938),(834,946),(789,951),(743,946),(707,936),(689,925),(688,914),(695,904),(670,890),(649,868),(631,840),(618,806),(613,768),(618,729),(631,689),(643,655),(651,636),(668,620),(699,608),(733,601)],
'cupcake':[(277,1040),(295,1044),(313,1059),(322,1081),(339,1092),(352,1116),(372,1127),(389,1149),(401,1173),(412,1197),(419,1220),(414,1242),(426,1256),(431,1280),(426,1302),(419,1321),(406,1352),(394,1383),(379,1412),(354,1424),(318,1432),(278,1437),(236,1433),(199,1423),(179,1409),(166,1375),(155,1345),(145,1315),(137,1284),(137,1266),(130,1251),(127,1232),(134,1210),(148,1197),(145,1180),(150,1158),(167,1138),(189,1120),(211,1107),(231,1089),(239,1062),(257,1045)],
'cupcake_bitten':[(767,1046),(787,1051),(805,1065),(812,1086),(829,1098),(839,1119),(849,1134),(868,1142),(880,1158),(884,1175),(869,1175),(856,1181),(849,1193),(850,1203),(841,1210),(841,1221),(834,1230),(836,1243),(848,1254),(846,1266),(862,1271),(876,1272),(878,1286),(873,1303),(865,1325),(855,1356),(840,1390),(828,1414),(804,1427),(770,1435),(729,1437),(689,1431),(657,1420),(640,1403),(630,1374),(620,1343),(611,1310),(610,1287),(618,1270),(610,1255),(611,1234),(620,1215),(632,1200),(633,1179),(644,1158),(662,1144),(681,1128),(705,1111),(719,1096),(722,1074),(738,1056)]}
sheet=Image.open(src/'portable_storybook_v2.png').convert('RGBA');portable={}
for name,points in contours.items():
 mask=Image.new('L',(sheet.width*4,sheet.height*4));ImageDraw.Draw(mask).polygon([(x*4,y*4) for x,y in points],fill=255)
 mask=mask.resize(sheet.size,Image.Resampling.LANCZOS)
 a=np.asarray(mask)>127
 # The contour is only a segmentation guide. Refine toward source edges without
 # changing any RGB pixels; preserve definite inner pixels and distant background.
 m=np.full(a.shape,cv2.GC_PR_BGD,dtype=np.uint8);m[a]=cv2.GC_PR_FGD
 m[ndi.binary_erosion(a,iterations=16)]=cv2.GC_FGD
 m[~ndi.binary_dilation(a,iterations=25)]=cv2.GC_BGD
 bgr=cv2.cvtColor(np.asarray(sheet)[:,:,:3],cv2.COLOR_RGB2BGR)
 cv2.grabCut(bgr,m,None,np.zeros((1,65)),np.zeros((1,65)),5,cv2.GC_INIT_WITH_MASK)
 alpha=ndi.binary_fill_holes((m==cv2.GC_FGD)|(m==cv2.GC_PR_FGD))
 alpha=ndi.binary_opening(alpha,iterations=6)
 alpha=ndi.binary_dilation(alpha,iterations=10)
 mask=Image.fromarray((alpha*255).astype('uint8'));bounds=mask.getbbox();card=sheet.copy();card.putalpha(mask);card=card.crop(bounds);card.save(fg/(name+'.png'))
 portable[name]={'bounds':bounds,'polygon':points,'mask':'hand contour guided OpenCV 4.10 GrabCut, 5 iterations, alpha only','sha256':hashlib.sha256((fg/(name+'.png')).read_bytes()).hexdigest()}
(src/'portable_masks.json').write_text(json.dumps(portable,indent=2)+'\n')
print('Saved original RGB pixels with explicit alpha contours')
