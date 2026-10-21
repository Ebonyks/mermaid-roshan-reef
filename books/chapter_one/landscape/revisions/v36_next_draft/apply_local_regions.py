"""Historical initial-mask authoring script; NOT a rebuild entry point. Use BOOK_CURRENT.json and render_book.py."""
"""Apply reviewed V36 local regions to preserved V34 scene bases."""
import json,hashlib
from pathlib import Path
from PIL import Image
L=Path(__file__).resolve().parents[2];V=Path(__file__).resolve().parent
b=json.loads((L/'book.json').read_text());P={p['page']:p for p in b['pages']}
def patch(n,id,poly,placement=None):
 f=V/'art'/f'{id}_attempt1.png';im=Image.open(f);key='v36_'+id
 b['sources'][key]={'file':f.relative_to(L).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'native_size':list(im.size),'provenance_record':'revisions/v36_next_draft/generation_evidence.json'}
 q={'source':key,'reference_size':list(im.size),'polygon':poly}
 if placement:q['placement']=placement
 if isinstance(n,int) and P[n].get('page_extension'):q['canvas_transform_points']=[0,0,504/im.width]
 target=b['cover'] if n=='cover' else P[n]
 target.setdefault('local_patches',[])[:]=[x for x in target.get('local_patches',[]) if x['source']!=key]
 target['local_patches'].append(q)
# Source-preserving bounded character regions. Masks deliberately exclude hands/contact.
patch('cover','c_cover',[[609,498],[645,488],[686,510],[704,532],[740,542],[785,508],[820,515],[833,553],[812,577],[795,619],[779,646],[755,698],[711,716],[661,664],[625,656],[618,629],[646,624],[645,578],[614,558]])
patch(1,'c01',[[266,25],[530,25],[550,180],[460,232],[372,232],[291,168]])
patch(1,'c01',[[397,260],[474,257],[531,331],[552,400],[550,459],[520,530],[438,548],[374,525],[384,469],[395,410]])
# two separate additions require append without replace for same source
# restore crown patch (patch helper above replaces prior source on same page).
P[1]['local_patches'].append({'source':'v36_c01','reference_size':[1484,1060],'polygon':[[266,25],[530,25],[550,180],[460,232],[372,232],[291,168]]})
patch(3,'c03',[[525,307],[751,307],[783,363],[775,416],[735,426],[723,476],[738,503],[700,525],[700,578],[650,616],[570,617],[523,552],[518,465]])
P[3]['local_patches'].append({'source':'v36_c03','reference_size':[1484,1060],'polygon':[[96,398],[103,331],[161,264],[200,212],[211,177],[348,177],[347,207],[263,220],[245,255],[215,287],[181,334],[128,415],[96,440]]})
patch(4,'c04',[[112,485],[133,470],[202,477],[224,501],[234,544],[220,568],[195,576],[195,546],[200,515],[186,496],[150,493],[126,515],[117,557],[108,557]])
patch(7,'c07',[[271,251],[284,214],[347,195],[390,204],[386,173],[395,140],[444,118],[501,128],[536,162],[539,194],[514,223],[482,238],[493,244],[544,257],[574,289],[610,332],[629,363],[658,376],[658,406],[629,425],[609,459],[574,484],[524,510],[446,520],[364,518],[297,506],[268,482],[278,447],[302,423],[312,381],[336,342],[373,312],[337,310],[295,304],[274,279]])
# small hair interior only, preserve sink silhouette exactly
patch(8,'c08',[[797,356],[783,314],[799,261],[813,230],[824,280],[820,334],[834,369],[829,389]],{'source':'approved_sink_action','box':P[8]['foreground_zone']})
patch(11,'c11',[[20,396],[114,365],[179,373],[220,427],[219,475],[210,520],[180,534],[173,605],[154,635],[97,631],[36,617],[15,568],[18,505]])
patch(15,'c15',[[730,280],[775,222],[843,207],[994,217],[1065,241],[1114,281],[1146,372],[1146,455],[1110,520],[1062,546],[1060,599],[1002,632],[973,596],[984,555],[1023,535],[1020,498],[993,474],[963,471],[962,427],[983,382],[974,321],[944,279],[888,263],[829,278],[790,315],[777,363],[771,410],[788,452],[781,485],[775,536],[785,563],[759,575],[732,535],[718,465],[719,407]])
patch(17,'c17',[[628,297],[670,285],[710,301],[752,341],[751,388],[707,413],[664,411],[646,380],[623,371],[613,334]],{'source':'v29_hug16','box':P[17]['foreground_zone']})
P[17]['local_patches'].append({'source':'v36_c17','reference_size':[1484,1060],'polygon':[[702,481],[752,479],[808,476],[838,485],[855,522],[845,567],[803,579],[760,567],[728,543]],'placement':{'source':'v29_hug16','box':P[17]['foreground_zone']}})
patch(18,'c18',[[736,267],[750,267],[754,287],[738,290]])
P[18]['local_patches'].append({'source':'v36_c18','reference_size':[1484,1060],'polygon':[[788,254],[800,254],[802,278],[788,278]]})
for n in [19,20]:
 patch(n,'c'+str(n),[[280,195],[430,183],[573,190],[620,232],[627,291],[608,320],[580,305],[560,284],[530,278],[493,290],[473,306],[455,335],[433,350],[426,377],[397,388],[386,416],[385,460],[355,482],[308,470],[278,430],[267,351]])
patch(23,'c23',[[824,514],[910,509],[957,522],[973,547],[953,552],[928,548],[916,565],[903,589],[899,615],[868,641],[826,648],[813,618],[816,576]])
patch(25,'c25',[[1030,80],[1247,58],[1385,103],[1492,173],[1513,304],[1468,421],[1393,465],[1322,446],[1316,415],[1296,397],[1265,377],[1287,340],[1294,299],[1278,259],[1262,243],[1254,190],[1213,170],[1169,176],[1145,211],[1121,235],[1106,283],[1116,336],[1143,355],[1141,376],[1164,434],[1119,475],[1065,442],[1040,357],[1024,281]],{'source':'v34_roshan_sponge_only','box':P[25]['foreground_zone']})
for n,poly in [(26,[[396,448],[448,443],[471,472],[448,484],[402,497]]),(27,[[396,448],[448,443],[471,472],[448,484],[402,497]]),(28,[[365,438],[416,434],[440,458],[414,474],[371,488]]),(29,[[395,438],[445,438],[469,463],[451,482],[399,494]])]:
 patch(n,'c'+str(n),poly)
for n,poly in [(28,[[1231,277],[1269,272],[1298,285],[1301,312],[1288,340],[1258,348],[1233,336],[1227,307]]),(29,[[1193,257],[1223,247],[1255,253],[1268,277],[1266,307],[1243,327],[1213,330],[1194,314],[1190,284]])]:
 P[n]['local_patches'].append({'source':'v36_c'+str(n),'reference_size':[1672,941],'canvas_transform_points':[0,0,504/1672],'polygon':poly})
patch(31,'c31',[[506,273],[540,272],[542,319],[509,322]],{'source':'v34_inviting_cutout','box':P[31]['placements'][0]['box']})
P[31]['local_patches'].append({'source':'v36_c31','reference_size':[1230,1278],'polygon':[[603,304],[640,304],[643,346],[604,348]],'placement':{'source':'v34_inviting_cutout','box':P[31]['placements'][0]['box']}})
# Refine masks to cover old and new local contours, preventing clipped remnants.
P[1]['local_patches']=[q for q in P[1]['local_patches'] if q['source']!='v36_c01']
P[1]['local_patches'].append({'source':'v36_c01','reference_size':[1484,1060],'polygon':[[220,0],[600,0],[609,294],[565,390],[560,478],[543,536],[504,558],[425,565],[368,548],[354,505],[365,438],[369,374],[389,310],[390,267],[345,235],[287,227],[228,166]]})
for q in P[3]['local_patches']:
 if q['source']=='v36_c03' and min(x for x,y in q['polygon'])>400:q['polygon']=[[517,307],[775,307],[793,381],[783,423],[741,425],[728,472],[739,495],[754,508],[744,527],[716,533],[706,579],[680,619],[631,623],[584,619],[522,562],[511,451]]
for q in P[11]['local_patches']:
 if q['source']=='v36_c11':q['polygon']=[[15,354],[182,353],[225,421],[224,478],[210,531],[180,539],[173,608],[160,652],[115,676],[52,670],[16,625],[5,538]]
for q in P[15]['local_patches']:
 if q['source']=='v36_c15':q['polygon']=[[719,284],[770,213],[847,190],[1000,204],[1075,228],[1149,293],[1164,438],[1137,533],[1085,585],[1064,636],[1001,644],[972,596],[984,556],[1023,536],[1020,498],[993,474],[963,471],[963,430],[983,382],[974,321],[936,299],[906,290],[878,278],[854,274],[833,284],[817,304],[800,326],[782,356],[774,411],[788,452],[781,485],[775,536],[785,563],[759,575],[727,539],[711,465],[710,407]]
# Reject visible rectangular dust/light joins. Keep evidence outside delivery.
b['cover']['local_patches']=[q for q in b['cover']['local_patches'] if q['source']!='v36_doorlight_attempt1']
P[4]['local_patches']=[q for q in P[4].get('local_patches',[]) if q['source']!='v36_dust4_attempt1']
P[3]['local_patches']=[q for q in P[3].get('local_patches',[]) if not q['source'].startswith('v36_dust')]
# Text is exact manuscript; only wrapping and positions change.
P[4]['caption'].update(x=218,y=104,width=260)
P[22]['placements'][0]['box']=[32,53,440,199]
P[22]['placements'][1]['box']=[250,132,25,12]
b['cover']['subtitle'].update(x=242,y=259,width=230,size=11)
rear=b['back_cover'];rear['story_scene_page']=3;rear['local_patches']=json.loads(json.dumps(P[3]['local_patches']))
rear['caption'].update(x=252,y=59,width=228,color='navy',outline=0)
proposal=json.loads((L/'revisions/v35_story_value/cover_proposal.json').read_text())['candidates'][0]['cameo']
b['sources']['v36_rear_lamma']={'file':'revisions/v35_story_value/art/lamma_head_attempt1.png','sha256':proposal['source_sha256']}
rear['cameo']={'source':'v36_rear_lamma','reference_size':[1484,1060],'clip_path':proposal['clip_path'],'transform':[1034,655,.022],'foreground_box':[1053,620,1090,715],'foreground_source':'v29_castle03'}
(L/'book.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
