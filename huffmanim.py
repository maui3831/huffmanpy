from manim import (
    Scene,
    Text,
    Write,
    Create,
    Table,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    LaggedStart,
    VGroup,
    FadeIn,
    FadeOut,
    Indicate,
    Flash,
    Rectangle,
    Line,
    YELLOW,
    WHITE,
    PINK,
    RED,
    ORANGE,
    BLUE,
    GREEN,
    BLUE_C,
    GREEN_C,
)
from manim.animation.transform import MoveToTarget
from manim.animation.creation import Create
import heapq
from collections import Counter
import numpy as np


# Helper class for Huffman Tree Nodes
class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char  # Character (None for internal nodes)
        self.freq = freq  # Frequency
        self.left = left  # Left child (HuffmanNode)
        self.right = right  # Right child (HuffmanNode)
        self.mobject = None  # Manim VGroup representing the node
        self.code = ""  # Huffman code (assigned during traversal)
        self.manim_pos = None  # Store target Manim position
        self.left_edge_mobject = None
        self.right_edge_mobject = None

    # For priority queue comparison
    def __lt__(self, other):
        if self.freq == other.freq:
            # Tie-breaking: prefer nodes with smaller character value (arbitrary but consistent)
            # Or prefer nodes created earlier (more complex to track without unique IDs)
            # For simplicity, if chars exist, compare them.
            if self.char is not None and other.char is not None:
                return self.char < other.char
            return False  # Fallback if one or both are internal or for identical frequencies
        return self.freq < other.freq


class HuffmanCodingScene(Scene):
    def construct(self, input_string="MANIM HUFFMAN DEMO"):
        if not input_string:
            self.add(Text("Input string is empty!", color=RED))
            self.wait(2)
            return

        title = Text("Huffman Coding: " + input_string, font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # --- 1. Frequency Calculation ---
        freq_map_title = (
            Text("1. Calculate Frequencies", font_size=28)
            .next_to(title, DOWN, buff=0.5)
            .to_edge(LEFT, buff=0.5)
        )
        self.play(Write(freq_map_title))

        frequencies = Counter(input_string)
        if not frequencies:
            self.add(
                Text("No characters to encode.", color=YELLOW).next_to(
                    freq_map_title, DOWN, aligned_edge=LEFT
                )
            )
            self.wait(2)
            return

        freq_table_data = [["Character", "Frequency"]] + [
            [f"'{char}'", str(count)] for char, count in sorted(frequencies.items())
        ]
        manim_freq_table = (
            Table(freq_table_data, include_outer_lines=True)
            .scale(0.5)
            .next_to(freq_map_title, DOWN, buff=0.3, aligned_edge=LEFT)
        )
        self.play(Create(manim_freq_table))
        self.wait(2)

        # --- 2. Priority Queue & Initial Leaf Nodes ---
        pq_title = Text("2. Create Leaf Nodes (Priority Queue)", font_size=28).next_to(
            manim_freq_table, DOWN, buff=0.7, aligned_edge=LEFT
        )
        self.play(Write(pq_title))

        priority_queue = []
        initial_leaf_mobjects_group = VGroup()
        # Create HuffmanNode objects and their initial mobjects
        for char, freq in sorted(frequencies.items()):
            node = HuffmanNode(char, freq)
            node.mobject = self._create_node_mobject(char, freq, is_leaf=True)
            heapq.heappush(priority_queue, node)
            initial_leaf_mobjects_group.add(node.mobject)

        initial_leaf_mobjects_group.arrange(RIGHT, buff=0.2).next_to(
            pq_title, DOWN, buff=0.3, aligned_edge=LEFT
        ).scale(0.8)
        for node in priority_queue:  # Ensure mobjects are where group is arranged
            node.mobject.generate_target()
        self.play(
            LaggedStart(
                *[Create(node.mobject) for node in priority_queue], lag_ratio=0.2
            )
        )
        self.wait(2)

        # Store all mobjects that will form the tree
        self.tree_mobjects_group = VGroup(*[node.mobject for node in priority_queue])

        # --- 3. Tree Construction ---
        build_tree_title = Text("3. Build Huffman Tree", font_size=28)
        # Position tree title based on where the tree will roughly be (center-ish)
        # This is a bit of a guess; adjust as needed
        build_tree_title.move_to(
            UP * 2.5 + RIGHT * 3.5
        )  # Adjusted to avoid overlap later

        # Animate clearing previous stage visuals (except title)
        self.play(
            FadeOut(freq_map_title),
            FadeOut(manim_freq_table),
            FadeOut(pq_title),
            # Move initial leaf nodes up to make space for the tree
            initial_leaf_mobjects_group.animate.scale(0.7).next_to(
                build_tree_title, DOWN, buff=0.5
            ),
            Write(build_tree_title),
        )
        self.wait(1)

        # Keep track of active nodes (mobjects) on screen that are part of the "queue"
        active_mobjects_on_screen = VGroup(*[node.mobject for node in priority_queue])

        merge_step = 1
        while len(priority_queue) > 1:
            step_text = Text(
                f"Step {merge_step}: Merge smallest", font_size=20
            ).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(step_text))

            # Extract two smallest
            node1 = heapq.heappop(priority_queue)
            node2 = heapq.heappop(priority_queue)

            # Highlight them
            highlight_color = YELLOW
            original_color1 = node1.mobject[0].get_color()  # Assuming rect is first
            original_color2 = node2.mobject[0].get_color()
            self.play(
                node1.mobject[0].animate.set_fill(highlight_color, opacity=0.5),
                node2.mobject[0].animate.set_fill(highlight_color, opacity=0.5),
                run_time=0.5,
            )
            self.wait(0.5)

            # Create parent node
            parent_freq = node1.freq + node2.freq
            parent_node = HuffmanNode(
                None, parent_freq, node1, node2
            )  # Assign children (left/right might be arbitrary here, or sort by freq)
            parent_node.mobject = self._create_node_mobject(
                None, parent_freq, is_leaf=False
            )
            self.tree_mobjects_group.add(parent_node.mobject)

            # Position parent mobject (initially, above and between children)
            # This is a temporary visual position for the merge animation
            temp_parent_pos = (
                node1.mobject.get_center() + node2.mobject.get_center()
            ) / 2 + UP * 1.0
            parent_node.mobject.move_to(temp_parent_pos)
            parent_node.mobject.set_opacity(0)  # Start transparent

            self.play(
                FadeIn(parent_node.mobject, shift=DOWN * 0.2),
                parent_node.mobject.animate.set_opacity(1),
                run_time=0.5,
            )

            # Create edges (will be repositioned later by _layout_tree_mobjects)
            edge1_temp = Line(
                parent_node.mobject.get_bottom(),
                node1.mobject.get_top(),
                stroke_width=2,
                color=WHITE,
            )
            edge2_temp = Line(
                parent_node.mobject.get_bottom(),
                node2.mobject.get_top(),
                stroke_width=2,
                color=WHITE,
            )
            parent_node.left_edge_mobject = edge1_temp  # Store for 0/1 labels
            parent_node.right_edge_mobject = edge2_temp

            self.tree_mobjects_group.add(edge1_temp, edge2_temp)
            self.play(Create(edge1_temp), Create(edge2_temp), run_time=0.5)

            # "Remove" children from active list and "add" parent
            active_mobjects_on_screen.remove(node1.mobject, node2.mobject)
            active_mobjects_on_screen.add(parent_node.mobject)

            # Rearrange active mobjects (conceptually, this is the PQ reordering)
            # For visualization, just arrange them simply
            self.play(
                active_mobjects_on_screen.animate.arrange(RIGHT, buff=0.3).next_to(
                    build_tree_title, DOWN, buff=0.5
                ),
                node1.mobject[0].animate.set_fill(
                    original_color1, opacity=0.5
                ),  # Assuming rect is first
                node2.mobject[0].animate.set_fill(original_color2, opacity=0.5),
                run_time=1,
            )

            heapq.heappush(priority_queue, parent_node)
            self.play(FadeOut(step_text))
            merge_step += 1
            self.wait(0.5)

        root_node = priority_queue[0]  # The final root

        # --- Layout the complete tree mobjects ---
        # Clear the temporary arrangement of active_mobjects_on_screen
        self.play(
            FadeOut(active_mobjects_on_screen - root_node.mobject)
        )  # Keep root mobj

        # Target position for the root of the tree
        tree_root_pos = build_tree_title.get_center() + DOWN * 2.0  # Adjust as needed

        # Calculate max depth for x_spacing_base
        max_depth = self._get_tree_depth(root_node)
        x_spacing_base = max(
            1.0, (self.camera.frame_width / (2**max_depth)) * 0.6
        )  # Heuristic

        self._calculate_positions_recursively(
            root_node,
            x=tree_root_pos[0],
            y=tree_root_pos[1],
            x_spacing_factor=x_spacing_base * (2 ** (max_depth - 1)),  # Wider at top
            y_spacing=1.2,
        )

        # Animate all tree components moving to their final calculated positions
        animations = []
        # First, collect all node and edge animations
        temp_edges_to_fadeout = (
            VGroup()
        )  # Edges created during build might be misaligned

        q = [root_node]
        visited_nodes_for_layout_anim = set()
        while q:
            curr_h_node = q.pop(0)
            if curr_h_node in visited_nodes_for_layout_anim or not curr_h_node.mobject:
                continue
            visited_nodes_for_layout_anim.add(curr_h_node)

            animations.append(
                curr_h_node.mobject.animate.move_to(curr_h_node.manim_pos)
            )

            if curr_h_node.left:
                if (
                    curr_h_node.left_edge_mobject
                ):  # If edge was created during merge step
                    temp_edges_to_fadeout.add(curr_h_node.left_edge_mobject)
                new_edge_left = Line(
                    curr_h_node.manim_pos
                    + DOWN * 0.25,  # From bottom of parent mobj (adjust offset)
                    curr_h_node.left.manim_pos
                    + UP * 0.25,  # To top of child mobj (adjust offset)
                    stroke_width=2,
                    color=WHITE,
                )
                curr_h_node.left_edge_mobject = new_edge_left  # Update with new edge
                self.tree_mobjects_group.add(new_edge_left)  # Add to main group
                animations.append(Create(new_edge_left))
                q.append(curr_h_node.left)

            if curr_h_node.right:
                if curr_h_node.right_edge_mobject:
                    temp_edges_to_fadeout.add(curr_h_node.right_edge_mobject)
                new_edge_right = Line(
                    curr_h_node.manim_pos + DOWN * 0.25,
                    curr_h_node.right.manim_pos + UP * 0.25,
                    stroke_width=2,
                    color=WHITE,
                )
                curr_h_node.right_edge_mobject = new_edge_right  # Update with new edge
                self.tree_mobjects_group.add(new_edge_right)  # Add to main group
                animations.append(Create(new_edge_right))
                q.append(curr_h_node.right)

        if temp_edges_to_fadeout:
            self.play(
                FadeOut(temp_edges_to_fadeout), run_time=0.1
            )  # Remove old edges quickly

        # Group animations: move nodes, then create new edges
        node_move_anims = [
            anim for anim in animations if isinstance(anim, MoveToTarget)
        ]
        edge_create_anims = [anim for anim in animations if isinstance(anim, Create)]

        if node_move_anims:
            self.play(*node_move_anims, run_time=1.5)
        if edge_create_anims:
            self.play(*edge_create_anims, run_time=1)

        self.wait(1)

        # --- 4. Code Generation ---
        code_gen_title = (
            Text("4. Generate Codes (0=Left, 1=Right)", font_size=24)
            .to_edge(LEFT, buff=0.5)
            .align_to(manim_freq_table, UP)
        )  # Reuse position
        self.play(
            FadeOut(build_tree_title),
            self.tree_mobjects_group.animate.scale(0.85).move_to(
                RIGHT * 2.5 + DOWN * 0.5
            ),  # Move tree to make space
            Write(code_gen_title),
        )

        codes = {}
        code_labels_group = VGroup()
        self._assign_codes_visual(root_node, "", codes, code_labels_group)
        self.wait(1)

        code_table_data = [["Character", "Code"]] + [
            [f"'{char}'", code] for char, code in sorted(codes.items())
        ]
        manim_code_table = (
            Table(code_table_data, include_outer_lines=True)
            .scale(0.45)
            .next_to(code_gen_title, DOWN, buff=0.3, aligned_edge=LEFT)
        )
        self.play(Create(manim_code_table))
        self.wait(2)

        # --- 5. Encoding ---
        encode_title = Text("5. Encode Original String", font_size=28).next_to(
            manim_code_table, DOWN, buff=0.7, aligned_edge=LEFT
        )
        self.play(Write(encode_title))

        original_str_text = Text(
            f"Original: {input_string}", font_size=20, t2c={"Original:": BLUE}
        ).next_to(encode_title, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(original_str_text))

        encoded_string = "".join(codes[char] for char in input_string)

        # Split encoded string for better display if too long
        max_len_per_line = 50
        encoded_parts = [
            encoded_string[i : i + max_len_per_line]
            for i in range(0, len(encoded_string), max_len_per_line)
        ]
        encoded_str_display = VGroup()
        first_line = True
        prev_line_mobj = original_str_text
        for i, part in enumerate(encoded_parts):
            prefix = (
                "Encoded: " if first_line else "         "
            )  # Align subsequent lines
            line_mobj = Text(
                prefix + part,
                font_size=20,
                t2c={"Encoded:": GREEN, "         ": GREEN, part: WHITE},
            )
            if first_line:
                line_mobj.next_to(prev_line_mobj, DOWN, buff=0.2, aligned_edge=LEFT)
                first_line = False
            else:
                line_mobj.next_to(prev_line_mobj, DOWN, buff=0.1, aligned_edge=LEFT)
            encoded_str_display.add(line_mobj)
            prev_line_mobj = line_mobj

        self.play(Write(encoded_str_display))
        self.wait(1)

        original_bits = (
            len(input_string) * 8
        )  # Assuming 8 bits per char (ASCII/UTF-8 basic)
        encoded_bits = len(encoded_string)
        savings_text_content = f"Original bits: {original_bits} (at 8 bits/char)\nEncoded bits: {encoded_bits}"
        if original_bits > 0:
            savings_percent = (1 - encoded_bits / original_bits) * 100
            savings_text_content += f"\nSavings: {savings_percent:.2f}%"

        savings_text = Text(savings_text_content, font_size=20)

        savings_text.next_to(encoded_str_display, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(savings_text))
        self.wait(3)

        # Final fade out or keep screen
        self.play(
            FadeOut(title),
            FadeOut(code_gen_title),
            FadeOut(manim_code_table),
            FadeOut(encode_title),
            FadeOut(original_str_text),
            FadeOut(encoded_str_display),
            FadeOut(savings_text),
            FadeOut(self.tree_mobjects_group),
            FadeOut(code_labels_group),
        )
        final_message = Text("Huffman Coding Complete!", font_size=36)
        self.play(Write(final_message))
        self.wait(2)
        self.play(FadeOut(final_message))

    def _create_node_mobject(self, char, freq, is_leaf=True, scale=0.6):
        """Creates a Manim VGroup for a Huffman node."""
        content_color = WHITE
        if is_leaf:
            char_text = f"'{char}'" if char else "Err"
            node_label = VGroup(
                Text(char_text, font_size=24, color=content_color),
                Text(str(freq), font_size=20, color=content_color),
            ).arrange(DOWN, buff=0.05)
            rect_color = BLUE_C
        else:  # Internal node
            node_label = Text(str(freq), font_size=20, color=content_color)
            rect_color = GREEN_C

        rect = Rectangle(
            width=node_label.width + 0.4,
            height=node_label.height + 0.3,
            color=rect_color,
            fill_color=rect_color,
            fill_opacity=0.5,
        )
        node_mobject = VGroup(rect, node_label).scale(scale)
        return node_mobject

    def _get_tree_depth(self, node):
        if node is None:
            return 0
        return 1 + max(
            self._get_tree_depth(node.left), self._get_tree_depth(node.right)
        )

    def _calculate_positions_recursively(
        self, h_node, x, y, x_spacing_factor, y_spacing=1.5, current_depth=0
    ):
        """
        Calculates and stores target Manim positions for nodes in h_node.manim_pos.
        x_spacing_factor is the horizontal distance between children at the current level.
        """
        if h_node is None:
            return

        h_node.manim_pos = np.array([x, y, 0])

        # Reduce x_spacing_factor for deeper levels
        child_x_spacing = x_spacing_factor / 2

        if h_node.left:
            self._calculate_positions_recursively(
                h_node.left,
                x - child_x_spacing,
                y - y_spacing,
                child_x_spacing,
                y_spacing,
                current_depth + 1,
            )

        if h_node.right:
            self._calculate_positions_recursively(
                h_node.right,
                x + child_x_spacing,
                y - y_spacing,
                child_x_spacing,
                y_spacing,
                current_depth + 1,
            )

    def _assign_codes_visual(self, node, current_code, codes_dict, code_labels_group):
        """Recursively assigns codes and animates adding 0/1 labels to edges."""
        if node is None:
            return

        node.code = current_code
        path_highlight_anims = []

        if node.char is not None:  # Leaf node
            codes_dict[node.char] = current_code
            # Highlight the leaf node
            if node.mobject:
                path_highlight_anims.append(
                    Indicate(node.mobject, color=PINK, scale_factor=1.2, run_time=0.7)
                )

        if (
            path_highlight_anims
        ):  # Play before recursing further for leaves or before adding edge labels
            self.play(*path_highlight_anims, run_time=0.7)
            # self.wait(0.3) # Short pause after highlighting a leaf's path

        if node.left:
            if node.left_edge_mobject:
                label_0 = Text("0", font_size=20, color=BLUE_C).move_to(
                    node.left_edge_mobject.get_center() + LEFT * 0.2 + UP * 0.1
                )
                code_labels_group.add(label_0)
                self.play(
                    Write(label_0),
                    Flash(
                        node.left_edge_mobject,
                        color=BLUE_C,
                        line_length=0.3,
                        flash_radius=0.5,
                    ),
                    run_time=0.5,
                )
            self._assign_codes_visual(
                node.left, current_code + "0", codes_dict, code_labels_group
            )

        if node.right:
            if node.right_edge_mobject:
                label_1 = Text("1", font_size=20, color=ORANGE).move_to(
                    node.right_edge_mobject.get_center() + RIGHT * 0.2 + UP * 0.1
                )
                code_labels_group.add(label_1)
                self.play(
                    Write(label_1),
                    Flash(
                        node.right_edge_mobject,
                        color=ORANGE,
                        line_length=0.3,
                        flash_radius=0.5,
                    ),
                    run_time=0.5,
                )
            self._assign_codes_visual(
                node.right, current_code + "1", codes_dict, code_labels_group
            )


# To run this scene from the command line:
# manim -pql huffman_script.py HuffmanCodingScene
# For a custom string:
# manim -pql huffman_script.py HuffmanCodingScene -a "YOUR STRING HERE"
# (The -a flag is a custom addition not standard in Manim for construct args,
#  you'd typically change the default value in the construct method or subclass)
# A simpler way for testing: in the script, change the default input_string value.

# Example of how to run with a different string by modifying the script:
# if __name__ == "__main__":
#     custom_string = "ABRACADABRA" # Or "TEST" or "HELLO WORLD"
#     config.output_file = f"HuffmanCoding_{custom_string.replace(' ','_')}"
#     scene = HuffmanCodingScene()
#     scene.construct(input_string=custom_string)
#
# To make the -a flag work, you'd typically integrate with a CLI argument parser
# or use Manim's plugin system if it supports direct argument passing to construct.
# For now, the easiest is to change the default `input_string` in the `construct` method.
