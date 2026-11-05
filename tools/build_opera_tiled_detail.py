#!/usr/bin/env python3
"""Assemble generated detail tiles, retaining original fixture geometry and palette."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/review/opera_exploration_v1/tiled_detail"
OUTPUT = ROOT / "assets/review/opera_tiled_detail_v1"

def digest(path):
	return hashlib.sha256(path.read_bytes()).hexdigest()

def pot(value):
	return 1 << (int(value)-1).bit_length()

def save_card(image, name):
	canvas = Image.new("RGBA", (pot(image.width), pot(image.height)), (0,0,0,0))
	canvas.paste(image, (0,0))
	path = OUTPUT / name
	canvas.save(path)
	return {"path":name, "texture_size":list(canvas.size), "sha256":digest(path)}

def axis_weight(start, end, core_start, core_end):
	values = np.arange(start,end,dtype=np.float32)+0.5
	weight = np.ones(len(values),dtype=np.float32)
	if core_start>start:
		weight *= np.clip((values-start)/(core_start-start),0,1)
	if core_end<end:
		weight *= np.clip((end-values)/(end-core_end),0,1)
	return weight

def fixture_details(original, ids):
	"""Use new surface information only where it agrees with the source layout."""
	groups = []
	plan_path = SOURCE/"object_detail_plan.json"
	if not plan_path.exists():
		return groups
	for item in json.loads(plan_path.read_text(encoding="utf-8"))["groups"]:
		path = SOURCE/item["output"]
		if not path.is_file():
			raise ValueError("Missing fixture detail: "+item["name"])
		raw = Image.open(path).convert("RGB")
		box = item["native_input_rect"]
		reference = original.crop(box).resize(raw.size,Image.Resampling.LANCZOS)
		blur = raw.filter(ImageFilter.GaussianBlur(2))
		error = np.abs(np.asarray(blur,dtype=np.float32)-np.asarray(reference.filter(ImageFilter.GaussianBlur(2)),dtype=np.float32)).mean(axis=2)
		confidence = np.exp(-error/12.0)
		detail = np.asarray(raw,dtype=np.float32)-np.asarray(blur,dtype=np.float32)
		pixels = np.clip(np.asarray(reference,dtype=np.float32)+detail*confidence[:,:,None]*0.95,0,255).astype("uint8")
		enhanced = Image.fromarray(pixels)
		enhanced_path = SOURCE/(item["id"]+"_registered.png")
		enhanced.save(enhanced_path)
		local_ids = Image.fromarray(ids[box[1]:box[3],box[0]:box[2]].astype("int32")).resize(raw.size,Image.Resampling.NEAREST)
		groups.append({"name":item["name"],"box":box,"image":enhanced,"ids":np.asarray(local_ids),"scale":[raw.width/(box[2]-box[0]),raw.height/(box[3]-box[1])],"parent":item["output"],"parent_sha256":digest(path),"registered_sha256":digest(enhanced_path),"confidence_mean":float(confidence.mean())})
	return groups

def containing_group(groups, box):
	return next((g for g in groups if g["box"][0]<=box[0] and g["box"][1]<=box[1] and g["box"][2]>=box[2] and g["box"][3]>=box[3]),None)

def main():
	plan = json.loads((SOURCE/"tile_plan.json").read_text(encoding="utf-8"))
	ownership = json.loads((SOURCE/"object_ownership.json").read_text(encoding="utf-8"))
	original_path = ROOT / ownership["source"]
	original = Image.open(original_path).convert("RGB")
	clean = Image.open(SOURCE/"clean_plate_raw.png").convert("RGB").resize(original.size,Image.Resampling.LANCZOS)
	ids = np.load(SOURCE/"object_ownership_ids.npy")
	# Heal owned interiors. Retain a two-source-pixel boundary under the same
	# source-owned edge to prevent resampling the unrelated clean support plane
	# into the surrounding original wall. No complete fitting remains beneath.
	base_native = np.asarray(original).copy()
	healed_interior = np.asarray(Image.fromarray((ids>0).astype("uint8")*255).filter(ImageFilter.MinFilter(5)))>0
	base_native[healed_interior] = np.asarray(clean)[healed_interior]
	base = Image.fromarray(base_native)
	width,height = plan["target_master_size"]
	density = min(width/1024,height/576)
	native_rows = []
	for tile in plan["tiles"]:
		path = SOURCE/"tile_outputs"/(tile["id"]+".png")
		if not path.is_file():
			raise ValueError("Missing native tile: "+tile["id"])
		with Image.open(path) as image:
			b = tile["original_bounds"]
			actual = min(image.width/(b[2]-b[0]),image.height/(b[3]-b[1]))
			native_rows.append({"id":tile["id"],"native_size":list(image.size),"native_density":actual,"source_sha256":digest(path)})
			if actual+0.01<density:
				raise ValueError("Insufficient native density: "+tile["id"])
	accum = np.zeros((height,width,3),dtype=np.float32)
	weights = np.zeros((height,width),dtype=np.float32)
	for tile in plan["tiles"]:
		b = tile["original_bounds"]
		c = tile["core_original_bounds"]
		x0,y0,x1,y1 = [round(b[0]/1024*width),round(b[1]/576*height),round(b[2]/1024*width),round(b[3]/576*height)]
		image = Image.open(SOURCE/"tile_outputs"/(tile["id"]+".png")).convert("RGB")
		if x1-x0>image.width or y1-y0>image.height:
			raise ValueError("Native tile would require enlargement")
		image = image.resize((x1-x0,y1-y0),Image.Resampling.LANCZOS)
		wx = axis_weight(x0,x1,c[0]/1024*width,c[2]/1024*width)
		wy = axis_weight(y0,y1,c[1]/576*height,c[3]/576*height)
		weight = wy[:,None]*wx[None,:]
		accum[y0:y1,x0:x1] += np.asarray(image,dtype=np.float32)*weight[:,:,None]
		weights[y0:y1,x0:x1] += weight
	if float(weights.min())<=0:
		raise ValueError("Background coverage gap")
	accum /= weights[:,:,None]
	merged = Image.fromarray(np.clip(accum,0,255).astype("uint8"))
	merged.save(SOURCE/"background_native_merged.png")
	del accum,weights
	# Preserve original layout and palette at low frequency. Only newly generated
	# fine surface information contributes; never retain invented semantic objects.
	low = np.asarray(merged.filter(ImageFilter.GaussianBlur(3)),dtype=np.float32)
	detail = np.asarray(merged,dtype=np.float32)-low
	del low
	anchor = base.resize((width,height),Image.Resampling.LANCZOS)
	# Keep source-card boundaries quiet; source pixels remain the sole fitting owner.
	union = Image.fromarray((ids>0).astype("uint8")*255)
	expanded = union.filter(ImageFilter.MaxFilter(17)).resize((width,height),Image.Resampling.BILINEAR)
	permit = 1-np.asarray(expanded,dtype=np.float32)/255.0
	registered = Image.fromarray(np.clip(np.asarray(anchor,dtype=np.float32)+detail*permit[:,:,None]*0.75,0,255).astype("uint8"))
	registered.save(SOURCE/"background_registered.png")
	del detail,permit,anchor,expanded,merged
	OUTPUT.mkdir(parents=True,exist_ok=True)
	cards = []
	for y in range(0,height,1024):
		for x in range(0,width,1024):
			rect = (x,y,min(x+1024,width),min(y+1024,height))
			row,col = y//1024,x//1024
			info = save_card(registered.crop(rect).convert("RGBA"),"background_%d_%d.png"%(row,col))
			info.update(id="DetailBackground_%d_%d"%(row,col),source_rect=[x,y,rect[2]-x,rect[3]-y],reference_size=[width,height],z_index=-30,role="native_generated_detail_background")
			cards.append(info)
	objects = []
	rgba = np.asarray(original.convert("RGBA")).copy()
	reconstruction = np.asarray(base).copy()
	groups = fixture_details(original,ids)
	for owner in ownership["objects"]:
		ident = owner["id"]
		owned = ids==ident
		reconstruction[owned] = np.asarray(original)[owned]
		x0,y0,x1,y1 = owner["native_rect"]
		group = containing_group(groups,[x0,y0,x1,y1])
		if group is None:
			pixels = rgba[y0:y1,x0:x1].copy()
			pixels[:,:,3] = np.where(owned[y0:y1,x0:x1],255,0).astype("uint8")
			object_image = Image.fromarray(pixels)
		else:
			gx,gy,_,_ = group["box"]
			sx,sy = group["scale"]
			crop = [round((x0-gx)*sx),round((y0-gy)*sy),round((x1-gx)*sx),round((y1-gy)*sy)]
			object_image = group["image"].crop(crop).convert("RGBA")
			pixels = np.asarray(object_image).copy()
			pixels[:,:,3] = np.where(group["ids"][crop[1]:crop[3],crop[0]:crop[2]]==ident,255,0).astype("uint8")
			object_image = Image.fromarray(pixels)
		object_density = [object_image.width/(x1-x0),object_image.height/(y1-y0)]
		virtual_reference = [original.width*object_density[0],original.height*object_density[1]]
		for sy in range(0,object_image.height,1024):
			for sx in range(0,object_image.width,1024):
				subrect=(sx,sy,min(sx+1024,object_image.width),min(sy+1024,object_image.height))
				name="source_"+owner["name"]+"_%d_%d.png"%(sy//1024,sx//1024)
				info=save_card(object_image.crop(subrect),name)
				info.update(id="OriginalFixture_"+owner["name"]+"_%d_%d"%(sy//1024,sx//1024),source_rect=[x0*object_density[0]+sx,y0*object_density[1]+sy,subrect[2]-sx,subrect[3]-sy],reference_size=virtual_reference,z_index=-29,role="source_locked_fixture_detail" if group else "preserved_original_fixture",owner=owner["name"],detail_parent=group["parent"] if group else None)
				objects.append(info)
	curtains = []
	for row,(top,bottom) in enumerate([(81,130),(205,252),(341,397)]):
		for col,x in enumerate([357,459,565,667]):
			world_box = [x-20,top,40,bottom-top]
			box = [int((x-20)*original.width/1024),int(top*original.height/576),int((x+20)*original.width/1024),int(bottom*original.height/576)]
			group = containing_group(groups,box)
			if group:
				gx,gy,_,_ = group["box"]
				sx,sy = group["scale"]
				crop = [round((box[0]-gx)*sx),round((box[1]-gy)*sy),round((box[2]-gx)*sx),round((box[3]-gy)*sy)]
				fabric = group["image"].crop(crop).convert("RGBA")
			else:
				fabric = original.crop(box).convert("RGBA")
			info = save_card(fabric,"curtain_%d_%d.png"%(row,col))
			info.update(original_bounds=world_box,native_rect=[0,0,fabric.width,fabric.height],detail_parent=group["parent"] if group else None)
			curtains.append(info)
	exact = bool(np.array_equal(reconstruction,np.asarray(original)))
	if not exact:raise ValueError("Source fixture reconstruction changed original pixels")
	layout={"version":2,"native_size":[width,height],"native_2k_per_screen":width/2>=2048 and height/2>=2048,"per_screen_native_background":[width/2,height/2],"method":"24 native generated detail tiles, overlap merge, source low-frequency lock; six source-locked fixture detail groups; one owner per fitting","source_object_native_size":list(original.size),"source_object_resolution_note":"Original source geometry/palette is retained as the low-frequency reference. Six regional native generations add registered surface detail; unsupported cross-group fixtures reuse their original source pixels, with their original resolution declared.","cards":cards,"objects":objects,"curtains":curtains}
	(OUTPUT/"layout.json").write_text(json.dumps(layout,indent=2)+"\n",encoding="utf-8")
	# Export round-trip verifies the actual cropped/padded runtime cards.
	roundtrip = Image.new("RGBA",(width,height))
	for card in cards:
		x,y,w,h=card["source_rect"]
		image=Image.open(OUTPUT/card["path"]).convert("RGBA")
		roundtrip.paste(image.crop((0,0,w,h)),(x,y))
	equal = bool(np.array_equal(np.asarray(roundtrip),np.asarray(registered.convert("RGBA"))))
	if not equal:raise ValueError("Runtime slice round-trip changed generated detail pixels")
	report={"target_native_size":[width,height],"per_screen_native_background":[width/2,height/2],"background_card_count":len(cards),"source_fixture_card_count":len(objects),"source_fixture_groups":len(ownership["objects"]),"native_tile_densities":native_rows,"minimum_generated_density":min(row["native_density"] for row in native_rows),"required_density":density,"source_fixture_reference_reconstruction_byte_exact":exact,"runtime_fixture_pixels_are_original_only":False,"fixture_detail_groups":[{k:g[k] for k in ("name","parent","parent_sha256","registered_sha256","confidence_mean")} for g in groups],"curtain_cards":len(curtains),"runtime_background_roundtrip_byte_exact":equal,"all_runtime_textures_pot":all(all(n&(n-1)==0 for n in a["texture_size"]) and max(a["texture_size"])<=1024 for a in cards+objects+curtains),"derivation":"Low-frequency source lock uses resized historical source for composition and palette; native generated high-frequency surfaces supply new detail. Fixture microdetail is source-confidence masked; this is a declared composite, not a claim that the historical master was native4K or that new runtime pixels equal the historical master.","new_semantic_objects":False,"original_source_sha256":digest(original_path),"native_master_sha256":digest(SOURCE/"background_native_merged.png"),"registered_master_sha256":digest(SOURCE/"background_registered.png"),"runtime_layout_sha256":digest(OUTPUT/"layout.json"),"visual_device_child_owner_acceptance":"PENDING"}
	(SOURCE/"assembly_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
	print(json.dumps({"size":[width,height],"per_screen":[width/2,height/2],"background_cards":len(cards),"source_cards":len(objects),"source_exact":exact,"runtime_roundtrip":equal}))

if __name__=="__main__":
	main()

