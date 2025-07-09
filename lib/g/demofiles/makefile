# Makefile to construct the examples in the output directory.  You'll
# want to have the g.py et. al. files in your PYTHONPATH.

files = \
	out/4x6_card.ps \
	out/bus_card_angle_measure.ps \
	out/cal_plain.ps \
	out/calendar.ps \
	out/center_contrast1.ps \
	out/center_contrast2.ps \
	out/color_by_color.ps \
	out/color_by_name.ps \
	out/colored_boxes.ps \
	out/degree_scale.ps \
	out/ellipses.ps \
	out/eng_grid1_1.ps \
	out/eng_grid1_2.ps \
	out/eng_grid1_3.ps \
	out/eng_grid2_2.ps \
	out/eng_grid2_3.ps \
	out/eng_grid21.ps \
	out/fill_eofill.ps \
	out/filled_path.ps \
	out/font_gallery1.ps \
	out/font_gallery2.ps \
	out/grid.ps \
	out/helloworld.ps \
	out/hsv_boxes.ps \
	out/illusion.ps \
	out/lines.ps \
	out/number_spiral.ps \
	out/paper_scale.ps \
	out/piddle_demo.ps \
	out/radial_text.ps \
	out/resolution_target.ps \
	out/resolution_target_gray.ps \
	out/rounded_rect.ps \
	out/symbols.ps \
	out/target_bb.ps \
	out/target_rifle.ps \
	out/text_path.ps \
	out/white.ps
all:  $(files)
out/%.ps: %.py
	python $<
out/center_contrast1.ps: center_contrast.py
	python $<
out/center_contrast2.ps: center_contrast.py
	python $<
out/color_by_color.ps: color_tables.py
	python $<
out/color_by_name.ps: color_tables.py
	python $<
out/eng_grid1_1.ps: eng_grid.py
	python $<
out/eng_grid1_2.ps: eng_grid.py
	python $<
out/eng_grid1_3.ps: eng_grid.py
	python $<
out/eng_grid2_2.ps: eng_grid.py
	python $<
out/eng_grid2_3.ps: eng_grid.py
	python $<
out/eng_grid21.ps: eng_grid.py
	python $<
out/font_gallery1.ps: font_gallery.py
	python $<
out/font_gallery2.ps: font_gallery.py
	python $<
clean:
	rm -f $(files)
# vim: noet
