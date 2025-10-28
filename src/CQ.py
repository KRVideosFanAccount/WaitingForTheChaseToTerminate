from coolerDiGraph import CoolDiGraph
from manim import *
import numpy as np

class CQ:
    def __init__(self, variables, constants, atoms, atom_colors=None):
        self.variables = variables
        self.constants = constants
        self.atoms = atoms
        self.atom_colors = atom_colors if atom_colors is not None else {}
        # Optional: validate that all atom arguments are in variables or constants
    
    def to_mathtex_parts(self):
        parts = []
        # Quantifier
        if self.variables:
            parts.append(r"\exists ")
            for i, v in enumerate(self.variables):
                parts.append(str(v))
                if i < len(self.variables) - 1:
                    parts.append(",")
            parts.append(r"\ \ ")
        # Atoms and connectives
        for i, atom in enumerate(self.atoms):
            pred = atom[0]
            args = list(map(str, atom[1:]))
            # Add predicate
            parts.append(pred)
            parts.append("(")
            for j, arg in enumerate(args):
                parts.append(arg)
                if j < len(args) - 1:
                    parts.append(",")
            parts.append(")")
            if i < len(self.atoms) - 1:
                parts.append(r"\wedge ")
        #parts.append(")")
        return parts
    
    def to_digraph(self, **kwargs):
        """
        Returns a CoolDiGraph representing the CQ (only for unary and binary predicates).
        Nodes: variables + constants
        Edges: predicates (colored according to atom_colors, with edge labels for predicates)
        Variables: blank label, Constants: label is the constant
        """
        nodes = list(set(self.variables) | set(self.constants))
        # Only binary predicates
        edges = [edge for edge in self.atoms if len(edge) == 3]
        # CoolDiGraph expects (role_name, u, v)
        role_edges = [(edge[0], edge[1], edge[2]) for edge in edges]

        # Edge config as a dict for per-edge coloring
        edge_config = {}
        edge_label_config = {}
        for edge in edges:
            color = self.atom_colors.get(edge[0], WHITE)
            edge_config[(edge[1], edge[2])] = {"color": color, 'stroke_width':2}
            edge_label_config[(edge[1], edge[2])] = {"labelFontSize": 24, "labelScale": 1.0, "labelOffset": 0.15}

        return CoolDiGraph(
            nodes,
            role_edges,
            edge_config=edge_config,
            edge_label_config=edge_label_config,
            labels=True,
            vertex_config={'fill_color': BLACK},
            **kwargs
        )

    def to_mathtex(self, return_parts=False):
        """
        Returns a MathTex object representing the full CQ as a single LaTeX string, using the parts from to_mathtex_parts.
        Colors each atom substring according to self.atom_colors.
        """
        parts = self.to_mathtex_parts()
        cq_tex = MathTex(*parts)
        # Color the atom submobjects in the MathTex
        atom_indices = []
        i = 0
        for atom in self.atoms:
            pred = atom[0]
            args = list(map(str, atom[1:]))
            while i < len(parts):
                if parts[i] == pred and i+2 < len(parts) and parts[i+1] == '(':  # crude check
                    atom_indices.append(i)
                    i += 6  # skip to next atom (for binary)
                    break
                i += 1
        for idx, atom in zip(atom_indices, self.atoms):
            color = self.atom_colors.get(atom[0], WHITE)
            for j in range(6):  # pred, (, arg1, ,, arg2, )
                cq_tex[idx + j].set_color(color)
        if return_parts:
            return cq_tex, parts
        return cq_tex

class CQExampleScene(Scene):
    def construct(self):
        # Example CQ: exists x, y (r(x, a) ∧ s(x, y))
        variables = ['x', 'y']
        constants = ['a']
        atoms = [
            ('r', 'x', 'a'),
            ('s', 'x', 'y'),
        ]
        atom_colors = {'r': RED, 's': BLUE}
        cq = CQ(variables, constants, atoms, atom_colors=atom_colors)

        # Render the LaTeX equation at the top
        cq_tex, parts = cq.to_mathtex(return_parts=True)
        cq_tex.scale(1.2)
        cq_tex.to_edge(UP)
        self.play(Write(cq_tex))

        # Render the invisible digraph below
        cq_graph = cq.to_digraph()
        cq_graph.next_to(cq_tex, DOWN*2)
        cq_graph.set_opacity(0)
        self.add(cq_graph)
        
        # Animate variables from MathTex to their node positions
        var_indices = []
        idx = 1  # After "\\exists "
        for v in variables:
            var_indices.append(idx)
            idx += 2  # Skip comma after each variable except last

        for v, i in zip(variables, var_indices):
            var_mob = cq_tex[i]
            var_copy = var_mob.copy()
            self.add(var_copy)
            self.play(var_copy.animate.move_to(cq_graph[v].get_center()), run_time=1)
            self.play(cq_graph[v][1].animate.set_opacity(1), run_time=0.3)
            self.remove(var_copy)

        # Animate constants from MathTex to their node positions
        const_indices = {}
        for c in constants:
            for i, part in enumerate(parts):
                if part == c:
                    const_indices[c] = i
                    break

        for c, i in const_indices.items():
            const_mob = cq_tex[i]
            const_copy = const_mob.copy()
            self.add(const_copy)
            self.play(const_copy.animate.move_to(cq_graph[c].get_center()), run_time=1)
            self.play(cq_graph[c][1].animate.set_opacity(1), run_time=0.3)
            self.remove(const_copy)

        # Find the start indices of each atom in the MathTex parts (for binary atoms)
        atom_indices = []
        i = 0
        for atom in atoms:
            pred = atom[0]
            args = list(map(str, atom[1:]))
            while i < len(parts):
                if parts[i] == pred and i+2 < len(parts) and parts[i+1] == '(':  # crude check
                    atom_indices.append(i)
                    i += 6  # skip to next atom (for binary)
                    break
                i += 1

        # Animate atoms from MathTex to their edge positions
        atom_groups = []
        edge_mobs = []
        for idx, atom in zip(atom_indices, atoms):
            pred, arg1, arg2 = atom
            atom_group = VGroup(*[cq_tex[idx + j] for j in range(6)])
            atom_group_copy = atom_group.copy()
            self.add(atom_group_copy)
            # Find the edge midpoint
            edge = (arg1, arg2)
            edge_mob = cq_graph.edges[edge]
            start = cq_graph[arg1].get_center()
            end = cq_graph[arg2].get_center()
            edge_mid = (start + end) / 2
            # Calculate angle
            vec = end - start
            angle = np.arctan2(vec[1], vec[0])
            # Animate move and rotation
            self.play(
                atom_group_copy.animate.move_to(edge_mid).rotate(angle, about_point=edge_mid),
                run_time=1
            )
            # Morph the atom group into the edge
            self.play(Transform(atom_group_copy, edge_mob), run_time=0.6)
            edge_mob.set_opacity(1)  # Instantly make the edge visible
            self.remove(atom_group_copy)
            atom_groups.append(atom_group)
            edge_mobs.append(edge_mob)

        # self.wait(1)
        
        # # Wiggle the red edge and r(x,a) atom together
        # self.play(
        #     Wiggle(atom_groups[0], scale_value=1.2),
        #     edge_mobs[0].animate.scale(1.2)
        # )
        # self.play(
        #     edge_mobs[0].animate.scale(1/1.2),
        # )
        # self.wait(1)
        # # Wiggle the blue edge and s(x,y) atom together
        # self.play(
        #     Wiggle(atom_groups[1], scale_value=1.2),
        #     edge_mobs[1].animate.scale(1.2)
        # )
        # self.play(
        #     edge_mobs[1].animate.scale(1/1.2),
        # )
        self.wait(4)
