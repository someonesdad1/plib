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

${file}: ${datafiles} ${tmp} ${script}
	${PYTHON} ${script} ${tmp} >${file}

${tmp}: ${datafiles}
	${PYTHON} g_lib_rgb.py >${tmp}
	${PYTHON} medium_color_database.py >>${tmp}
	${PYTHON} name_that_color.py >>${tmp}
	${PYTHON} raveling.py >>${tmp}
	${PYTHON} resene_pencils.py >>${tmp}
	${PYTHON} resenecolors.py >>${tmp}
	${PYTHON} wikipedia_list.py >>${tmp}
	${PYTHON} xfree_rgb.py >>${tmp}
	${PYTHON} xkcd_rgb.py >>${tmp}

clean:
	rm ${tmp}
