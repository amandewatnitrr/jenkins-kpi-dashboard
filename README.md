graph TD
  A[Extract URLs from Config Files] -->|List of URLs| B(Process Each Repository)
  B -->|Fetch Jenkinsfile| C{Branch Available?}
  C -- Yes -->|Process Jenkinsfile| D{Jenkinsfile Found?}
  D -- Yes -->|Extract Libraries| E(Update Library Counts)
  D -- No -->|Log Missing Jenkinsfile| F(Log Missing Jenkinsfile)
  C -- No -->|Log No Branch Found| G(Log No Branch Found)
  E -->|Log Library Usage| H(Update 'libraries_by_repo.csv')
  B -->|Finish Processing Repositories| I(Finish)

  subgraph Main Process
    A --> B --> C
    E --> H
  end

  subgraph Asynchronous Operations
    B -->|Async Fetch| C
    C -->|Async Fetch| D
    D -->|Async Fetch| E
    C -->|Async Log| F
    C -->|Async Log| G
    E -->|Async Log| H
  end

  subgraph CSV Files
    H -->|Update| I
  end

  subgraph Logging
    F -->|Log| I
    G -->|Log| I
  end
