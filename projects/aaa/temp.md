```mermaid
graph TD
    A[Start] -->|Check Data| B{Funerary}
    B -->|Yes| C[Set Funerary/Memorial]
    B -->|No| D{Domestic}
    C -->|Update| E[Medium Certainty, Tomb/Grave/Burial]
    D -->|Yes| F[Set Domestic]
    D -->|No| G{Agricultural}
    F -->|Update| H[Medium Certainty, House/Dwelling]
    G -->|Yes| I[Set Agricultural/Pastoral]
    G -->|No| J{Industrial}
    I -->|Update| K[Medium Certainty, Farm]
    J -->|Yes| L[Set Industrial/Productive]
    J -->|No| M{Hydrological}
    L -->|Update| N[Medium Certainty, Press/Press Element]
    M -->|Yes| O[Set Hydrological]
    M -->|No| P{Religious}
    O -->|Update| Q[Medium Certainty, Aqueduct]
    P -->|Yes| R[Set Religious]
    P -->|No| S{Defensive}
    R -->|Update| T[Medium Certainty, Church/Chapel]
    S -->|Yes| U[Set Defensive/Fortification]
    S -->|No| V{Classical}
    U -->|Update| W[Medium Certainty, Fort/Fortress/Castle]
    V -->|Yes| X[Set Classical/Protohistoric/Pre-Islamic]
    V -->|No| Y{Berber}
    X -->|Update| Z[Possible Certainty]
    Y -->|Yes| AA[Set Unknown]
    Y -->|No| AB[End]
    AA -->|Update| AC[Not Applicable Certainty]
    E --> AB
    H --> AB
    K --> AB
    N --> AB
    Q --> AB
    T --> AB
    W --> AB
    Z --> AB
    AC --> AB
```

```mermaid
graph TD
    A[Start] -->|Check Data| B{Funerary}
    B -->|Yes| C[Set Funerary/Memorial]
    B -->|No| D{Domestic}
    C -->|Update| E[Tomb/Grave/Burial]
	E --> EZ(Medium Certainty)
    D -->|Yes| F[Set Domestic]
    D -->|No| G{Agricultural}
    F -->|Update| H[House/Dwelling]
	H --> HZ(Medium Certainty)
    G -->|Yes| I[Set Agricultural/Pastoral]
    G -->|No| J{Industrial}
    I -->|Update| K[Farm]
	I --> IZ(Medium Certainty)
    J -->|Yes| L[Set Industrial/Productive]
    J -->|No| M{Hydrological}
    L -->|Update| N[Press/Press Element]
	L --> LZ(Medium Certainty)
    M -->|Yes| O[Set Hydrological]
    M -->|No| P{Religious}
    O -->|Update| Q[Aqueduct]
	O --> OZ(Medium Certainty)
    P -->|Yes| R[Set Religious]
    P -->|No| S{Defensive}
    R -->|Update| T[Church/Chapel]
	H --> TZ(Medium Certainty)
    S -->|Yes| U[Set Defensive/Fortification]
    S -->|No| V{Classical}
    U -->|Update| W[Fort/Fortress/Castle]
	W --> WZ(Medium Certainty)
    V -->|Yes| X[Set Classical/Protohistoric/Pre-Islamic]
    V -->|No| Y{Berber}
    X -->|Update| Z[Possible Certainty]
    Y -->|Yes| AA[Set Unknown]
    AA -->|Update| AC[Not Applicable Certainty]
```
```mermaid
graph TD
    A[Start] -->|Check Data| B{Funerary}
    subgraph subgraph1
    C[Set Funerary/Memorial]
    F[Set Domestic]
    I[Set Agricultural/Pastoral]
    L[Set Industrial/Productive]
    O[Set Hydrological]
    R[Set Religious]
    U[Set Defensive/Fortification]
    X[Set Classical/Protohistoric/Pre-Islamic]
    AA[Set Unknown]
    end
    B -->|Yes| C
    B -->|No| D{Domestic}
    C -->|Update| E[Tomb/Grave/Burial]
    E --> EZ(Medium Certainty)
    D -->|Yes| F
    D -->|No| G{Agricultural}
    F -->|Update| H[House/Dwelling]
    H --> HZ(Medium Certainty)
    G -->|Yes| I
    G -->|No| J{Industrial}
    I -->|Update| K[Farm]
    K --> KZ(Medium Certainty)
    J -->|Yes| L
    J -->|No| M{Hydrological}
    L -->|Update| N[Press/Press Element]
    N --> NZ(Medium Certainty)
    M -->|Yes| O
    M -->|No| P{Religious}
    O -->|Update| Q[Aqueduct]
    Q --> QZ(Medium Certainty)
    P -->|Yes| R
    P -->|No| S{Defensive}
    R -->|Update| T[Church/Chapel]
    T --> TZ(Medium Certainty)
    S -->|Yes| U
    S -->|No| V{Classical}
    U -->|Update| W[Fort/Fortress/Castle]
    W --> WZ(Medium Certainty)
    V -->|Yes| X
    V -->|No| Y{Berber}
    X -->|Update| Z[Possible Certainty]
    Y -->|Yes| AA
    AA -->|Update| AC[Not Applicable Certainty]
```

```mermaid
graph TD
    A[Start] -->|Check Data| B{Funerary}
    subgraph subgraph1
    C[Set Funerary/Memorial]
    F[Set Domestic]
    I[Set Agricultural/Pastoral]
    L[Set Industrial/Productive]
    O[Set Hydrological]
    R[Set Religious]
    U[Set Defensive/Fortification]
    X[Set Classical/Protohistoric/Pre-Islamic]
    AA[Set Unknown]
    end
    B -->|Yes| C
    B -->|No| D{Domestic}
    C -->|Update| E[Tomb/Grave/Burial]
    E --> EZ(Medium Certainty)
    D -->|Yes| F
    D -->|No| G{Agricultural}
    F -->|Update| H[House/Dwelling]
    H --> HZ(Medium Certainty)
    G -->|Yes| I
    G -->|No| J{Industrial}
    I -->|Update| K[Farm]
    K --> KZ(Medium Certainty)
    J -->|Yes| L
    J -->|No| M{Hydrological}
    L -->|Update| N[Press/Press Element]
    N --> NZ(Medium Certainty)
    M -->|Yes| O
    M -->|No| P{Religious}
    O -->|Update| Q[Aqueduct]
    Q --> QZ(Medium Certainty)
    P -->|Yes| R
    P -->|No| S{Defensive}
    R -->|Update| T[Church/Chapel]
    T --> TZ(Medium Certainty)
    S -->|Yes| U
    U -->|Update| W[Fort/Fortress/Castle]
    W --> WZ(Medium Certainty)
```