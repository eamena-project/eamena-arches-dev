```mermaid
flowchart LR
  subgraph EAMENA
	id1[University of Oxford]
	id2[University of Leicester]
	id3[University of Durham]
  end
  id1 ---> id6[The Database]
  id2 ---> id6
  id3 ---> id6
  subgraph MAREA
    id4[University of Southampton]
	id5[Ulster University]
  end
  id4 ---> id6
  id5 ---> id6

  click id1 "https://www.ox.ac.uk/" _blank
```