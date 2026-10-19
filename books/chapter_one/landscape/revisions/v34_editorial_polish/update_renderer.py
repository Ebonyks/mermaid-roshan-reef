from pathlib import Path
P=Path(__file__).resolve().parents[2]/'render_book.py'
s=P.read_text('utf8')
def change(a,b):
 global s
 assert a in s,a;s=s.replace(a,b)
change('source-preserving 7 x 5 inch landscape review book','source-preserving landscape review book at declared physical scale')
change("PDF=O/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';c=canvas.Canvas(str(PDF),pagesize=(W,H));", "S=float(B.get('physical_review_scale',1))\nPDF=O/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf';c=canvas.Canvas(str(PDF),pagesize=(W*S,H*S));")
change("c.setAuthor('Mermaid Roshan picture-book project')", "c.setAuthor('Mermaid Roshan picture-book project');c.scale(S,S)\ndef finish_page():\n c.showPage();c.scale(S,S)")
change(" im=Image.open(path(k));assert im.mode=='RGBA' and im.getextrema()[3][0]==0,k\n box=B['sources'][k].get('alpha_box')", " im=Image.open(path(k));contour=B['sources'][k].get('contour_polygon')\n assert (im.mode=='RGBA' and im.getextrema()[3][0]==0) or contour,k\n box=B['sources'][k].get('source_box') or B['sources'][k].get('alpha_box')")
change("text('A Pearl Castle friendship story',24,28,456,13,True)\nc.showPage()", "subtitle=B.get('cover',{}).get('subtitle',dict(text='A Pearl Castle friendship story',x=24,y=28,width=456,size=13))\ntext(subtitle['text'],subtitle['x'],subtitle['y'],subtitle['width'],subtitle['size'],True)\nfinish_page()")
change("  if p.get('page_extension'):page_extension(p)", "  if p.get('top_extension'):\n   q=p['top_extension'];h=q['height'];visible_strip(q['source'],q['source_box'],(0,H-h,W,h));region(a[0],(0,0,*Image.open(path(a[0])).size),(0,-h,W,H))\n  elif p.get('page_extension'):page_extension(p)")
change(" c.showPage()\nPAGE='back_cover'", " finish_page()\nPAGE='back_cover'\nback_transform=B['back_cover'].get('view_transform')\nif back_transform:\n c.saveState();cliprect(0,0,W,H);c.translate(*back_transform['translate']);c.scale(back_transform['scale'],back_transform['scale'])")
change("c.showPage();c.save()", "if back_transform:c.restoreState()\nif B['back_cover'].get('caption'):\n q=B['back_cover']['caption'];text(q['text'],q['x'],q['y'],q['width'],q['size'],True,color=q['color'],outline=q.get('outline',0))\nfinish_page();c.save()")
change("'page_size_points':[W,H]", "'page_size_points':[W*S,H*S],'logical_layout_points':[W,H],'logical_to_physical_scale':S,'rear_view_transform':back_transform")
change('page.render(scale=3)', 'page.render(scale=3/S)')
change("7 × 5 inches · 32 story pages + covers · ", "'+str(7*S)+' × '+str(5*S)+' inches · 32 story pages + covers · ")
change("'points':[W,H]", "'points':[W*S,H*S],'logical_layout_points':[W,H]")
P.write_text(s,encoding='utf8',newline='\n')
print('Physical2x review scale and source-contour isolation supported; historical default remains1x.')
