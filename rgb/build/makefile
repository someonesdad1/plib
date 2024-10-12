# vim: noet
#
# Construct the rgbdata.py file

file = rgbdata.py
script = build.py
tmp = rgbdata.tmp

datafiles = \
	g_lib_rgb.py \
	medium_color_database.py \
	name_that_color.py \
	raveling.py \
	resene_pencils.py \
	resenecolors.py \
	wikipedia_list.py \
	xfree_rgb.py \
	xkcd_rgb.py

${file}: clean ${datafiles} ${tmp} ${script}
	python ${script} ${tmp} >${file}
	#rm ${tmp}

${tmp}: ${datafiles}
	python g_lib_rgb.py >${tmp}
	python medium_color_database.py >>${tmp}
	python name_that_color.py >>${tmp}
	python raveling.py >>${tmp}
	python resene_pencils.py >>${tmp}
	python resenecolors.py >>${tmp}
	python wikipedia_list.py >>${tmp}
	python xfree_rgb.py >>${tmp}
	python xkcd_rgb.py >>${tmp}

clean:
	rm -f ${tmp}
