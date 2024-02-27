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
    end
    B -->|Yes| C
    B -->|No| D{Domestic}
    subgraph subgraph2
    E[Tomb/Grave/Burial]
    H[House/Dwelling]
    K[Farm]
    N[Press/Press Element]
    Q[Aqueduct]
    T[Church/Chapel]
    W[Fort/Fortress/Castle]
    end
    C -->|Update| E
    E --> EZ(Medium Certainty)
    D -->|Yes| F
    D -->|No| G{Agricultural}
    F -->|Update| H
    H --> HZ(Medium Certainty)
    G -->|Yes| I
    G -->|No| J{Industrial}
    I -->|Update| K
    K --> KZ(Medium Certainty)
    J -->|Yes| L
    J -->|No| M{Hydrological}
    L -->|Update| N
    N --> NZ(Medium Certainty)
    M -->|Yes| O
    M -->|No| P{Religious}
    O -->|Update| Q
    Q --> QZ(Medium Certainty)
    P -->|Yes| R
    P -->|No| S{Defensive}
    R -->|Update| T
    T --> TZ(Medium Certainty)
    S -->|Yes| U
    U -->|Update| W
    W --> WZ(Medium Certainty)
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
    end
    B -->|Yes| C
    B -->|No| D{Domestic}
    subgraph subgraph2
    E[Tomb/Grave/Burial]
    H[House/Dwelling]
    K[Farm]
    N[Press/Press Element]
    Q[Aqueduct]
    T[Church/Chapel]
    W[Fort/Fortress/Castle]
    end
    C -->|Update| E
    E --> EZ(Medium Certainty)
    D -->|Yes| F
    D -->|No| G{Agricultural}
    F -->|Update| H
    H --> HZ(Medium Certainty)
    G -->|Yes| I
    G -->|No| J{Industrial}
    I -->|Update| K
    K --> KZ(Medium Certainty)
    J -->|Yes| L
    J -->|No| M{Hydrological}
    L -->|Update| N
    N --> NZ(Medium Certainty)
    M -->|Yes| O
    M -->|No| P{Religious}
    O -->|Update| Q
    Q --> QZ(Medium Certainty)
    P -->|Yes| R
    P -->|No| S{Defensive}
    R -->|Update| T
    T --> TZ(Medium Certainty)
    S -->|Yes| U
    U -->|Update| W
    W --> WZ(Medium Certainty)
    subgraph subgraph3
    EZ(Medium Certainty)
    HZ(Medium Certainty)
    KZ(Medium Certainty)
    NZ(Medium Certainty)
    QZ(Medium Certainty)
    TZ(Medium Certainty)
    WZ(Medium Certainty)
    end
```

```mermaid
graph TD
    A[Start] -->|Check Data| B{Funerary}
    subgraph subgraph1
    C[Funerary/Memorial]
    F[Domestic]
    I[Agricultural/Pastoral]
    L[Industrial/Productive]
    O[Hydrological]
    R[Religious]
    U[Defensive/Fortification]
    end
    B -->|Yes| C
    B -->|No| D{Domestic}
    subgraph subgraph2
    E[Tomb/Grave/Burial]
    H[House/Dwelling]
    K[Farm]
    N[Press/Press Element]
    Q[Aqueduct]
    T[Church/Chapel]
    W[Fort/Fortress/Castle]
    end
    C --> E
    E --> EZ(Medium Certainty)
    D -->|Yes| F
    D -->|No| G{Agricultural}
    F --> H
    H --> HZ(Medium Certainty)
    G -->|Yes| I
    G -->|No| J{Industrial}
    I --> K
    K --> KZ(Medium Certainty)
    J -->|Yes| L
    J -->|No| M{Hydrological}
    L --> N
    N --> NZ(Medium Certainty)
    M -->|Yes| O
    M -->|No| P{Religious}
    O --> Q
    Q --> QZ(Medium Certainty)
    P -->|Yes| R
    P -->|No| S{Defensive}
    R --> T
    T --> TZ(Medium Certainty)
    S -->|Yes| U
    U --> W
    W --> WZ(Medium Certainty)
    subgraph subgraph3
    EZ(Medium Certainty)
    HZ(Medium Certainty)
    KZ(Medium Certainty)
    NZ(Medium Certainty)
    QZ(Medium Certainty)
    TZ(Medium Certainty)
    WZ(Medium Certainty)
    end
```

```mermaid
graph TD
    subgraph AAA
    A[Start] -->|Check Data| B{Funerary}
    end

    subgraph EAMENA
        subgraph subgraph1
        C[Funerary/Memorial]
        F[Domestic]
        I[Agricultural/Pastoral]
        L[Industrial/Productive]
        O[Hydrological]
        R[Religious]
        U[Defensive/Fortification]
        end
        B -->|Yes| C
        B -->|No| D{Domestic}
        subgraph subgraph2
        E[Tomb/Grave/Burial]
        H[House/Dwelling]
        K[Farm]
        N[Press/Press Element]
        Q[Aqueduct]
        T[Church/Chapel]
        W[Fort/Fortress/Castle]
        end
        C --> E
        E --> EZ(Medium Certainty)
        D -->|Yes| F
        D -->|No| G{Agricultural}
        F --> H
        H --> HZ(Medium Certainty)
        G -->|Yes| I
        G -->|No| J{Industrial}
        I --> K
        K --> KZ(Medium Certainty)
        J -->|Yes| L
        J -->|No| M{Hydrological}
        L --> N
        N --> NZ(Medium Certainty)
        M -->|Yes| O
        M -->|No| P{Religious}
        O --> Q
        Q --> QZ(Medium Certainty)
        P -->|Yes| R
        P -->|No| S{Defensive}
        R --> T
        T --> TZ(Medium Certainty)
        S -->|Yes| U
        U --> W
        W --> WZ(Medium Certainty)
        subgraph subgraph3
        EZ(Medium Certainty)
        HZ(Medium Certainty)
        KZ(Medium Certainty)
        NZ(Medium Certainty)
        QZ(Medium Certainty)
        TZ(Medium Certainty)
        WZ(Medium Certainty)
        end
    end
```