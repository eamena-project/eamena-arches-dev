import os
import re

# paste here the validation error message
text = """
0	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
0	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
1	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
1	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
2	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
3	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
3	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
4	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
4	Invalid concept value 'probable'
Did you mean 'Probable'?
4	Invalid concept value 'probable'
Did you mean 'Probable'?
5	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
5	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
5	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
5	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
5	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
5	Invalid concept value 'possible'
Did you mean 'Possible'?
5	Invalid concept value 'possible'
Did you mean 'Possible'?
5	Invalid concept value 'Human movement/Trampling'
Did you mean 'Human Movement/Trampling'?
6	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
6	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
6	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
7	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
7	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
8	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
8	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
9	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
10	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
10	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
11	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
11	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
12	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
12	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
12	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
13	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
14	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
15	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
15	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
16	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
17	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
18	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
19	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
20	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
21	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
22	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
22	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
22	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
23	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
24	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
25	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
26	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
27	Invalid concept value "Linear" for "Site Feature Shape Type".
Valid values: 'Curvilinear', 'Sub-circular', 'Sub-rectangular', 'Unknown', 'Circular', 'Semi-circular', 'Straight', 'Irregular', 'Multiple', 'Polygonal', 'Zigzag', 'Triangular', 'Rectangular/Square', 'Rectilinear', 'Winding'.
27	Invalid concept value "Rectangular" for "Site Feature Shape Type".
Valid values: 'Curvilinear', 'Sub-circular', 'Sub-rectangular', 'Unknown', 'Circular', 'Semi-circular', 'Straight', 'Irregular', 'Multiple', 'Polygonal', 'Zigzag', 'Triangular', 'Rectangular/Square', 'Rectilinear', 'Winding'.
27	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
27	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
28	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
29	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
30	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
31	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
33	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
34	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
35	Missing Location Certainty
Record cannot have a geometry without a location certainty.
36	Missing Location Certainty
Record cannot have a geometry without a location certainty.
37	Missing Location Certainty
Record cannot have a geometry without a location certainty.
38	Missing Location Certainty
Record cannot have a geometry without a location certainty.
39	Missing Location Certainty
Record cannot have a geometry without a location certainty.
40	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
41	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
42	Missing Location Certainty
Record cannot have a geometry without a location certainty.
43	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
44	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
44	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
44	Invalid concept value 'Recession of water'
Did you mean 'Recession of Water'?
45	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
45	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
45	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
46	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
46	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
47	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
47	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
48	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
48	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
48	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
48	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
48	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
48	Invalid concept value 'Human movement/Trampling'
Did you mean 'Human Movement/Trampling'?
49	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
50	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
51	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
52	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
53	Missing Location Certainty
Record cannot have a geometry without a location certainty.
54	Missing Location Certainty
Record cannot have a geometry without a location certainty.
55	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
55	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
55	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
55	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
55	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
56	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
57	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
57	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
57	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
58	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
58	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
59	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
59	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
60	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
60	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
60	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
60	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
60	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
60	Invalid concept value 'Human movement/Trampling'
Did you mean 'Human Movement/Trampling'?
61	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
61	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
61	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
62	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
62	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
63	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
63	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
63	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
64	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
64	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
65	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
65	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
65	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
65	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
66	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
66	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
67	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
67	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
68	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
69	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
69	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
69	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
70	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
70	No effect type or certainty.
Each disturbance in a condition assessment must have an effect type and an effect certainty. These can be Unknown and Not Applicable respectively, but may not be left blank.
70	Invalid concept value 'Human movement/Trampling'
Did you mean 'Human Movement/Trampling'?
"""

# Use regular expressions to add line breaks before integers
formatted_text = re.sub(r'(\d+)', r'\n * \1 ', text)

file_path = os.getcwd() + "\\data\\bulk\\bu_validation_error_message.md"

# Open the file in write mode and write the formatted text to it
with open(file_path, "w") as file:
    file.write(formatted_text)