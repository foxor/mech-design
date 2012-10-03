all : mech_design_graph.png best_mechanics

mech_design_graph.png : dotfile
	cat dotfile | neato -Tpng > mech_design_graph.png
	cp mech_design_graph.png /var/www-ij/

best_mechanics : centrality.py dotfile
	./centrality.py > best_mechanics
