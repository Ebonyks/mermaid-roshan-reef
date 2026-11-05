"""Apply evaluated V33 corrections without replacing complete source scenes."""
from pathlib import Path
from copy import deepcopy
from PIL import Image
import json,hashlib,shutil
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
G=Path('C:/Users/Peter/.codex/generated_images/01a0bd6a-0b70-7682-bd4c-44a20e6eed2d')
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=read(V/'BOOK_BASELINE.json');P={p['page']:p for p in b['pages']};records=read(V/'native_outputs_all.json')
# Reject unrecorded intermediate selection, retain every native attempt separately.
for q in records:
 p=V/'art'/f"{q['id']}_attempt{q['attempt']}.png";shutil.copy2(G/q['filename'],p)
 q.update(path=p.relative_to(R).as_posix(),sha256=sha(p),native_size=list(Image.open(p).size))
def add(id,attempt=1):
 k='v34_'+id;p=V/'art'/f'{id}_attempt{attempt}.png'
 b['sources'][k]=dict(file=p.relative_to(L).as_posix(),sha256=sha(p),native_size=list(Image.open(p).size),provenance_record='revisions/v34_editorial_polish/generation_evidence.json');return k
def patch(id,poly,attempt=1,**kw):return dict(source=add(id,attempt),reference_size=[1484,1060],polygon=poly,**kw)
def put(n,text,**kw):
 P[n]['text']=text;P[n]['caption']['size']=20;P[n]['caption'].update(kw)
for p in P.values():p['caption']['size']=20;p['caption']['outline']=.7 if p['caption']['color']=='white' else 0
b['physical_review_scale']=2;b['format_note']='14x10-inch landscape review: existing7:5 composition preserved at2x vector scale, no raster upsample. Final trim/bleed and high-resolution pass pending.'
b['revision']='V34 editorial polish';b['review_href']='../AUDIT_REVIEW.html';b['status']='Reviewed illustration/layout proof; final resolution and owner/child/print acceptance pending.'
b['cover']['subtitle']=dict(text='A Pearl Castle friendship story',x=142,y=260,width=338,size=13)
# Crown safety: exact source shifted8logical points down; only empty metal top strip supplied by candidate.
P[1]['top_extension']=dict(source=add('arrival_border'),source_box=[0,0,1484,20],height=8)
put(1,'“Look, Daddy!\nPearl Castle!”',x=292,y=60,width=182,color='navy',outline=0)
put(2,'The plane landed at Sky Lagoon.\nPearl Castle was close by.')
put(3,'“Let’s look inside,\nDaddy,” said Roshan.',x=275,y=57,width=200)
P[3]['local_patches']=[patch('entry_dust',[[777,485],[811,455],[850,459],[887,496],[917,544],[957,580],[1000,609],[1047,632],[1054,697],[1004,742],[952,748],[900,730],[843,736],[798,720],[769,685],[772,628]])]
put(5,'Inside, cobwebs hung high.\n“Let’s clean it together!”\nsaid Roshan.',x=226,y=90,width=248)
put(6,'Daddy gave her a duster and sponges.\n“One little job at a time,” he said.')
put(7,'A dust bunny splashed in the dirty bath.\nIt loved to play. Splash, splash!',x=30,y=54,width=444)
P[8]['foreground_zone']=[91,62,380,218]
put(8,'Round and round went the sponge.\nRoshan wiped the sink clean.')
P[9]['foreground_zone']=[27,58,394,212]
put(9,'Out went the dirty bath water.\nRoshan scrubbed the tub. Scrub, scrub!')
put(10,'Clean water filled the bath.\nThe dust bunny was ready to play!')
put(11,'Rumi was stuck under the gunk.\nShe needed help!',x=171,y=57,width=303,color='navy',outline=0)
P[11]['local_patches'].append(patch('pink_cup',[[1170,350],[1185,339],[1210,334],[1223,340],[1226,359],[1210,380],[1187,383],[1168,371]]))
put(12,'“I’ll help!” said Roshan.\nShe scooped out the rubbish. Scoop, scoop!')
P[12]['background_patches']=[patch('rubbish_bank',[[1004,918],[1045,910],[1113,914],[1157,939],[1174,974],[1146,1027],[1073,1032],[1012,1003]])]
P[12]['integrated_motifs']=['torn_star_wrapper','torn_blue_snack_bag','discarded_blue_cap'];P[12]['integrated_prop_bounds']=[[.2083,.8727,.0936,.0981],[.69,.874,.10,.095],[.8093,.8981,.0694,.0726]]
put(13,'Rainbow colors peeped through the gunk.',x=32,y=40,width=440,color='white',outline=.85)
put(14,'Whoosh! A rainbow waterfall!\nThe pool’s magic made rainbow water.',x=30,y=57,width=444,color='navy',outline=0)
put(15,'A cup was stuck in the fountain.\nRoshan pulled it free. Whoosh!')
put(16,'Up came Rumi. She was free!\nShe had lived here for hundreds of years.',x=30,y=58,width=444,color='navy',outline=0)
put(17,'“You helped me!”\nsaid Rumi.\nShe gave Roshan\na great big hug.',x=40,y=267,width=148)
put(18,'Chirp, chirp!\nThe sound came from the playroom.',x=30,y=58,width=444)
P[18].setdefault('local_patches',[]).append(patch('listening_face',[[716,249],[743,238],[773,243],[802,259],[814,283],[806,313],[782,337],[746,339],[716,321],[703,289]]))
put(19,'Two dust bunnies wanted to play.\nBut Baby Eagle was stuck beneath them!',x=33,y=62,width=438)
put(20,'Roshan gently brushed one bunny away,\nthen the other. Baby Eagle was free!',x=33,y=60,width=438)
put(21,'“Let’s play gently,” said Roshan.')
put(22,'In the art room, paints were everywhere.\nRoshan put them back. Tidy, tidy!')
P[22]['background_patches']=[patch('tidy_art_bank',[[194,916],[276,906],[354,916],[429,958],[430,1011],[376,1029],[221,1025],[188,985]],4),patch('tidy_art_bank',[[1083,921],[1152,911],[1217,911],[1296,922],[1303,996],[1262,1035],[1141,1036],[1087,1008]],4)]
P[22]['integrated_motifs']=['two_closed_sketchbooks','sketchbook_ribbon','folded_paint_cloth','tied_waste_paper'];P[22]['marginal_bunny_count']=0;P[22]['integrated_prop_bounds']=[[.137,.875,.104,.071],[.746,.9,.077,.054],[.825,.874,.045,.074]]
put(23,'One last door was still shut.\nRoshan stopped to listen.',x=40,y=56,width=424)
P[23]['caption'].update(color='navy',outline=0)
P[23]['local_patches'].append(patch('mysterious_door',[[1180,632],[1189,451],[1203,403],[1240,367],[1296,346],[1346,365],[1382,402],[1407,451],[1408,638]]))
put(24,'Grand Puff!\nHe was covered in dust.\nHe did not feel well.',x=45,y=257,width=215)
P[24]['background_patches']=[patch('care_bank24',[[1042,890],[1099,884],[1198,884],[1309,892],[1345,938],[1342,1010],[1289,1033],[1105,1038],[1044,1011]],3)]
P[24]['integrated_motifs']=['attic_chest','attic_book_stack','little_puff_tissue','little_puff_water_flask'];P[24]['integrated_prop_bounds']=[[.1044,.8537,.0828,.084],[.1899,.8792,.0761,.067],[.731,.85,.073,.097],[.823,.85,.075,.097],[.765,.915,.032,.038],[.8,.901,.025,.045]]
P[24]['background_theme']='Two little puffs gently prepare tissue and water; Grand Puff is foreground only.'
# The original alpha artwork contains two disconnected objects; isolate the complete Roshan only.
b['sources']['v34_roshan_sponge_only']=dict(b['sources']['v29_sponge25'],alpha_box=[887,55,1774,856],isolation='Whole source Roshan/sponge group; excludes disconnected Puff; no mirroring or new pose.')
P[25]['art']=['v34_roshan_sponge_only'];P[25]['foreground_zone']=[93,62,345,215]
put(25,'“Hold on, we’ll make you feel\nclean and better!” said Roshan.')
P[25]['background_patches']=[patch('care_bank25_focus',[[1157,965],[1171,958],[1193,960],[1207,971],[1208,1002],[1192,1008],[1168,1003],[1157,985]],source_canvas_box=[1045,909,1250,1028]),patch('care_bank25_focus',[[1056,916],[1082,914],[1086,945],[1061,947]],source_canvas_box=[1045,909,1250,1028])]
P[25]['integrated_motifs']=['attic_jar','attic_books','small_star','sofa','little_puff_waiting_to_help','little_puff_folding_washcloth','folded_washcloth','small_plant'];P[25]['background_theme']='Original little puffs keep their tiny sofa staging; cloth replaces popcorn, cheering marks removed.'
for n in [26,27,28,29]:P[n]['caption']['outline']=.85
put(27,'Soft bubbles covered Grand Puff.\nLittle colors began to shine beneath them.')
P[27]['local_patches']=[patch('foam_glints',[[645,451],[663,449],[685,462],[681,485],[655,486],[642,472]]),patch('foam_glints',[[771,514],[794,511],[810,525],[807,547],[782,546],[767,532]]),patch('foam_glints',[[724,678],[744,677],[757,696],[750,716],[729,716],[716,697]])]
put(30,'The art room was tidy. The castle was clean.\nOne little job at a time!',y=58)
P[31]['art']=['v34_inviting_cutout','approved_rainbow_puff_cutout'];P[31]['placements']=[dict(source=add('inviting_cutout'),box=[248,61,220,203]),dict(source='approved_rainbow_puff_cutout',box=[91,75,146,163])]
P[31]['local_patches'][0]['placement']['box']=[91,75,146,163]
put(31,'“We helped your rainbow shine!” said Roshan.\n“Thank you!” said Grand Puff.\n“Come and rest with us!”')
put(32,'There was room for everyone.\nThey curled up in bubbles and fell asleep.',x=40,y=320,width=424)
# Source-only physical door cutout, not the generated object with changed hardware.
door_poly=[[1175,804],[1185,652],[1181,631],[1183,445],[1194,404],[1216,371],[1251,348],[1288,335],[1321,348],[1357,367],[1388,404],[1404,446],[1405,633],[1411,650],[1431,800],[1423,817],[1166,817]]
b['sources']['v34_closed_door']=dict(b['sources']['v27_door'],source_box=[1166,335,1431,817],contour_polygon=door_poly,isolation='Document contour isolates whole physical castle door/arch/stair base from original RGB; transparent outside shape, no scene rectangle; original hardware preserved.')
new23=dict(page=23,mode='C',art=['v34_closed_door'],layout='wide_cut',text='A soft voice came from behind the door.\n“Can you help me?”',caption=dict(x=42,y=270,width=220,size=20,align='left',color='navy',shadow=False,halo=False,outline=0),foreground_zone=[279,62,163,225],border_assets=[],border_placements=[],integrated_background='v29_bank24_final',background_patches=[patch('quiet_bank',[[134,898],[205,898],[315,913],[371,948],[365,1018],[288,1032],[152,1021],[132,984]],2),patch('quiet_bank',[[1038,892],[1154,884],[1272,882],[1404,898],[1432,964],[1420,1036],[1280,1045],[1129,1039],[1042,1009]],2)],integrated_motifs=['little_puff_listening','closed_attic_books','shell_on_books'],integrated_prop_bounds=[[.112,.867,.055,.065],[.808,.876,.112,.074],[.849,.852,.041,.05]],marginal_bunny_count=1,background_theme='One tiny listening little puff echoes the quiet plea; closed books suggest the dusty attic. No Grand Puff in the banks.',beat='quiet_plea_before_reveal',original_page=None)
b['pages']=[P[n] for n in range(1,4)]+[P[n] for n in range(5,24)]+[new23]+[P[n] for n in range(24,33)]
mapping=[]
for n,p in enumerate(b['pages'],1):
 old=p['page'];mapping.append(dict(new=n,baseline_v33=old if p is not new23 else None,beat=p.get('beat')));p['page']=n
b['back_cover']['view_transform']=dict(scale=1.08,translate=[-20.16,-8])
b['back_cover']['caption']=dict(text='A castle to clean.\nA friend to help.',x=32,y=322,width=440,size=20,color='white',outline=.85)
assert len(b['pages'])==32 and b['pages'][27]['art']==['R10_jump'] and b['pages'][28]['art']==['R11_land']
save(L/'book.json',b);save(V/'BOOK_CURRENT.json',b);save(V/'pagination.json',mapping)
save(V/'generation_evidence.json',dict(count=len(records),native_attempts=records,method='20 built-in candidates; only accepted bounded polygons, source-derived object restoration and tiny marginal art used. Original scenes remain bases; all rejects and originals preserved. Prompts/roles before calls in generation_jobs_first_plan, generation_jobs, size_repair_jobs, final_local_jobs and quiet_size_job.',wrong_identity_rejection='Both first bank studies accidentally referenced Grand Puff; rejected on owner correction. All final marginal figures use only little puffs.',door_rejection='Generated object changed hardware. Final quiet page uses actual source RGB with a document contour, not generated replacement.',format=b['format_note']))
print('V34 manuscript applied;32 interiors plus covers, quiet plea23 and unchanged jump/landing28/29.')
