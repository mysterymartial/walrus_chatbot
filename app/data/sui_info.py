# ======================
# app/data/sui_info.py
# ======================

"""
Basic information about SUI blockchain and its key concepts.
This serves as a fallback when external search services cannot provide information.
"""

SUI_BLOCKCHAIN_INFO = {
    "what_is_sui": """
SUI is a Layer 1 blockchain and smart contract platform implemented in Rust. It is designed to enable creators and developers to build experiences that cater to the next billion users in Web3. 

Key characteristics of SUI include:

1. High throughput and low latency: SUI can process over 120,000 transactions per second (TPS) with sub-second finality.

2. Horizontal scalability: SUI's architecture allows it to scale horizontally by adding more resources, unlike traditional blockchains that face scalability limitations.

3. Object-centric model: SUI uses an object-centric data model rather than an account-based model, enabling parallel execution of transactions that touch different objects.

4. Move programming language: SUI uses the Move language for smart contracts, which was originally developed for the Diem blockchain. Move is designed with safety and security as primary considerations.

5. Proof-of-Stake consensus: SUI uses a delegated proof-of-stake consensus mechanism called Narwhal and Bullshark for high throughput and Byzantine fault tolerance.

SUI is also the name of the native token of the Sui blockchain, which is used for paying gas fees, staking, and governance.
""",
    
    "sui_token": """
SUI is the native token of the Sui blockchain. It serves several key functions within the ecosystem:

1. Gas fees: SUI is used to pay for transaction fees on the network.

2. Staking: Token holders can stake their SUI to validators to help secure the network and earn staking rewards.

3. Governance: SUI token holders can participate in on-chain governance decisions through the Sui governance system.

4. Storage fund: A portion of transaction fees goes into a storage fund that compensates validators for storing data on the blockchain.

SUI has a total supply of 10 billion tokens, with a portion allocated to early backers, the Sui Foundation, and the core contributors (Mysten Labs).
""",
    
    "sui_architecture": """
Sui's architecture is designed for high throughput and scalability through several innovative approaches:

1. Object-centric data model: Unlike account-based blockchains, Sui treats on-chain assets as distinct objects that can be operated on in parallel when there are no dependencies between transactions.

2. Consensus mechanism: Sui uses a two-part consensus mechanism:
   - Narwhal: A mempool and efficient data availability engine
   - Bullshark: A Byzantine Fault Tolerant (BFT) consensus protocol

3. Transaction types:
   - Simple transactions: Can be executed without global consensus
   - Complex transactions: Require consensus when they affect shared objects

4. Validator nodes: Responsible for processing transactions and maintaining the blockchain state

5. Full nodes: Store the blockchain state and serve read requests

6. Epoch-based operation: The network operates in epochs (24 hours), during which the validator set remains constant

This architecture allows Sui to achieve horizontal scalability, where performance increases as more resources are added to the network.
""",
    
    "move_language": """
Move is the programming language used for developing smart contracts on the Sui blockchain. It was originally created for the Diem blockchain and has been adapted for use in Sui.

Key features of Move include:

1. Safety-focused design: Move is designed to prevent common security vulnerabilities found in other smart contract languages.

2. Resource-oriented programming: Move treats assets as first-class resources that cannot be copied or implicitly discarded, only moved between storage locations.

3. Static type system: Move's type system helps catch many errors at compile time rather than runtime.

4. Formal verification: Move's design facilitates formal verification of smart contracts, allowing developers to mathematically prove properties about their code.

5. Module system: Code is organized into modules that define structured data types and functions that operate on those types.

6. Sui-specific extensions: Sui extends Move with additional features like dynamic fields and object-centric programming models.

Move's focus on safety and resource management makes it particularly well-suited for financial applications and managing digital assets.
""",
    
    "sui_objects": """
Objects are the fundamental unit of storage in Sui. They have the following characteristics:

1. Globally unique ID: Each object has a unique identifier across the entire blockchain.

2. Owner: Objects can be owned by:
   - An address (owned objects)
   - Another object (wrapped objects)
   - Shared (accessible by anyone)
   - Immutable (cannot be modified)

3. Version: Objects have a version number that increases with each transaction that modifies them.

4. Data fields: Objects contain data fields defined by their Move type.

5. Transaction execution: 
   - Transactions on owned objects can be executed in parallel
   - Transactions on shared objects require consensus

6. Dynamic fields: Objects can have fields added or removed dynamically, unlike traditional Move structs.

Sui's object-centric model enables high throughput by allowing parallel execution of transactions that touch different objects.
""",
    
    "sui_transactions": """
Transactions in Sui represent operations that modify the blockchain state. They have several key characteristics:

1. Transaction types:
   - Single-owner transactions: Can be certified by a single validator and don't require consensus
   - Shared-object transactions: Require consensus through the Narwhal and Bullshark protocols

2. Transaction structure:
   - Sender: The address initiating the transaction
   - Gas payment: Object used to pay for gas
   - Transaction data: The actual operation to perform
   - Gas price and budget: Maximum gas price and budget
   - Signatures: Cryptographic signatures authorizing the transaction

3. Transaction lifecycle:
   - Submission: User submits a transaction
   - Validation: Validators check the transaction's validity
   - Execution: The transaction is executed, modifying objects
   - Certification/Consensus: Transaction is certified by validator(s)
   - Finalization: Changes are committed to the blockchain

4. Gas model: Sui uses a gas model to charge for computational resources, storage, and network usage.

Sui's transaction model enables high throughput by allowing independent transactions to be processed in parallel.
""",
    
    "sui_consensus": """
Sui uses a novel consensus mechanism that combines two components:

1. Narwhal: A mempool and data availability engine that:
   - Efficiently disseminates transactions among validators
   - Ensures data availability with Byzantine fault tolerance
   - Creates a directed acyclic graph (DAG) of transactions

2. Bullshark: A Byzantine Fault Tolerant (BFT) consensus protocol that:
   - Operates on the DAG created by Narwhal
   - Achieves consensus finality quickly
   - Tolerates up to f Byzantine validators in a system with 3f+1 total validators

Key features of Sui's consensus approach:

1. Separate execution from consensus: Simple transactions can bypass consensus entirely

2. Epoch-based operation: The validator set is fixed during an epoch (typically 24 hours)

3. Stake-weighted voting: Validators' votes are weighted by their staked SUI

4. Finality: Transactions achieve finality within 2-3 seconds

5. Throughput: The system can process over 120,000 transactions per second

This dual approach allows Sui to achieve both high throughput and Byzantine fault tolerance.
""",
    
    "sui_storage": """
Sui's storage model is designed for efficiency and scalability:

1. Object-based storage: All on-chain data is stored as objects with unique IDs

2. Storage fund: A portion of transaction fees goes into a storage fund that compensates validators for storing data

3. Storage rebates: When objects are deleted, a portion of their storage fee is rebated

4. Merkle tree: Sui uses a Merkle tree structure to efficiently verify the state of objects

5. Dynamic fields: Objects can have fields added or removed dynamically, allowing for flexible data structures

6. Storage hierarchy:
   - Validators store the full state
   - Full nodes store the full state to serve read requests
   - Light clients only store a subset of data relevant to them

7. State synchronization: Nodes can efficiently synchronize state using Narwhal's data availability layer

This storage model supports Sui's high throughput and scalability goals while maintaining security and efficiency.
""",
    
    "sui_smart_contracts": """
Smart contracts in Sui are written in the Move programming language and have several distinctive features:

1. Module structure: Smart contracts are organized as Move modules containing:
   - Struct definitions (object types)
   - Functions that operate on those structs
   - Constants and other module members

2. Object capabilities: Access control is managed through capability objects that grant specific permissions

3. Entry functions: Public functions that can be called directly in transactions

4. Object-oriented approach: Smart contracts operate on objects with unique IDs

5. Publishing process:
   - Compile Move code to bytecode
   - Publish the module to the Sui blockchain
   - Initialize any necessary objects

6. Upgradeability: Sui supports upgradeable smart contracts through:
   - Upgrade capabilities
   - Package upgrades that preserve object compatibility

7. Testing framework: Sui provides a comprehensive testing framework for Move modules

8. Security features:
   - Type safety
   - Resource safety
   - Module isolation
   - Formal verification support

Sui's smart contract model combines the safety of Move with the scalability benefits of Sui's object-centric approach.
""",

    "sui_epochs": """
Sui Epochs are fundamental time periods that govern the Sui blockchain's operation:

What are Sui Epochs:
- Epochs are fixed time periods (typically 24 hours) that define network cycles
- Each epoch has a specific set of active validators
- Epochs ensure network decentralization through validator rotation
- Epoch boundaries trigger validator set updates and reward distributions

Sui Epoch Functions:
- Validator Set Management: Determines which validators are active in each epoch
- Reward Distribution: Validators receive rewards at epoch boundaries
- Network Security: Regular validator rotation prevents centralization
- Consensus Updates: Network parameters can be updated at epoch boundaries
- Transaction Processing: Epochs track transaction processing and finality

Sui Epoch Lifecycle:
- Epoch Start: New validator set becomes active
- Epoch Progress: Validators process transactions and maintain consensus
- Epoch End: Rewards distributed, validator set updated
- Epoch Transition: Smooth handover to next epoch's validators

Sui Epoch Information:
- Current epoch number and remaining time
- Active validators for current epoch
- Epoch rewards and stake distribution
- Historical epoch data and statistics
- Epoch-based network performance metrics

Real-time Sui epoch information is available through Sui Scan APIs, showing current epoch, remaining time, and validator details.
""",

    "sui_objects": """
Sui Objects are the fundamental data structures in the Sui blockchain:

What are Sui Objects:
- Objects are the primary data containers in Sui's object-centric model
- Each object has a unique ID and belongs to an owner
- Objects can be shared, owned, or immutable
- Objects contain data and can have associated functions

Object Types:
- Owned Objects: Belong to a specific address and can be transferred
- Shared Objects: Can be accessed by multiple transactions simultaneously
- Immutable Objects: Cannot be modified after creation
- Wrapped Objects: Objects that contain other objects

Object Properties:
- Object ID: Unique identifier for each object
- Owner: Address that owns the object (or shared/immutable)
- Version: Tracks object modifications and updates
- Digest: Cryptographic hash of object content
- Type: Defines the object's structure and capabilities

Object Operations:
- Create: Generate new objects with initial data
- Transfer: Move objects between addresses
- Update: Modify object data and properties
- Delete: Remove objects from the network
- Share: Make objects accessible to multiple users

Object Lifecycle:
- Creation: Objects are created through transactions
- Modification: Objects can be updated by their owners
- Transfer: Objects can be moved between addresses
- Sharing: Objects can be made accessible to multiple users
- Deletion: Objects can be removed when no longer needed
""",

    "move_smart_contracts": """
Move Smart Contracts are programs that run on the Sui blockchain:

What are Move Smart Contracts:
- Move is a programming language designed for blockchain applications
- Smart contracts define the logic and behavior of blockchain applications
- Move contracts are secure, efficient, and easy to audit
- Contracts can create, modify, and transfer digital assets

Move Language Features:
- Resource-oriented: Focuses on ownership and transfer of resources
- Linear types: Ensures resources are used exactly once
- Module system: Organizes code into reusable components
- Type safety: Prevents common programming errors
- Formal verification: Supports mathematical proof of correctness

Smart Contract Components:
- Modules: Contain function definitions and data structures
- Functions: Define the behavior and operations of the contract
- Structs: Define data structures and resource types
- Constants: Define immutable values used throughout the contract
- Events: Emit information about contract execution

Contract Development:
- Writing: Create Move modules with functions and structs
- Testing: Verify contract behavior with unit tests
- Deployment: Publish contracts to the Sui network
- Interaction: Call contract functions through transactions
- Upgrading: Modify contracts while maintaining compatibility

Move Security Features:
- Resource safety: Prevents double-spending and resource leaks
- Type safety: Catches errors at compile time
- Access control: Restricts function access to authorized users
- Formal verification: Supports mathematical proof of correctness
- Auditability: Code is transparent and verifiable
""",

    "what_is_blockchain": """
Blockchain is a distributed ledger technology that maintains a continuously growing list of records (blocks) that are linked and secured using cryptography:

What is Blockchain:
- A distributed ledger that records transactions across multiple computers
- Each block contains a cryptographic hash of the previous block
- Creates an immutable chain of data that cannot be altered retroactively
- Operates without a central authority, making it decentralized
- Uses consensus mechanisms to validate and add new blocks

Key Characteristics:
- Decentralization: No single point of control or failure
- Immutability: Data cannot be changed once recorded
- Transparency: All transactions are visible to network participants
- Security: Cryptographic hashing ensures data integrity
- Consensus: Network participants agree on the state of the ledger

Blockchain Components:
- Blocks: Containers that hold transaction data
- Hash: Cryptographic fingerprint of block data
- Previous Hash: Links blocks together in a chain
- Timestamp: When the block was created
- Nonce: Number used in mining process
- Merkle Tree: Efficient way to verify transaction integrity

Use Cases:
- Cryptocurrencies: Digital currencies like Bitcoin, Ethereum
- Smart Contracts: Self-executing contracts with predefined rules
- Supply Chain: Track products from origin to consumer
- Identity Management: Secure digital identity systems
- Voting Systems: Transparent and tamper-proof voting
- Healthcare: Secure patient data management
""",

    "types_of_blockchain": """
There are several types of blockchain networks, each with different characteristics and use cases:

Public Blockchains:
- Open to anyone: Anyone can join, read, and write data
- Decentralized: No single entity controls the network
- Examples: Bitcoin, Ethereum, Sui
- Benefits: Transparency, censorship resistance, global access
- Drawbacks: Lower transaction speeds, higher energy consumption

Private Blockchains:
- Restricted access: Only authorized participants can join
- Centralized control: Single organization manages the network
- Examples: Hyperledger Fabric, R3 Corda
- Benefits: Higher performance, privacy, regulatory compliance
- Drawbacks: Less decentralized, requires trust in central authority

Consortium Blockchains:
- Semi-decentralized: Controlled by a group of organizations
- Permissioned: Only pre-approved entities can participate
- Examples: Banking consortiums, supply chain networks
- Benefits: Balance of decentralization and control
- Drawbacks: Limited participation, potential for collusion

Hybrid Blockchains:
- Combination: Mix of public and private elements
- Flexible: Can switch between public and private modes
- Examples: Some enterprise solutions
- Benefits: Best of both worlds, customizable
- Drawbacks: Complexity, potential security issues

Blockchain Classifications:
- Permissionless vs Permissioned: Who can participate
- Public vs Private: Who can view the data
- Centralized vs Decentralized: Who controls the network
- Open vs Closed: Who can develop applications
""",

    "distributed_ledger": """
A Distributed Ledger is a database that is consensually shared and synchronized across multiple sites, institutions, or geographies:

What is a Distributed Ledger:
- A database spread across multiple locations or participants
- All participants have access to the same data
- Changes are reflected in all copies in real-time
- No central administrator or centralized data storage
- Uses consensus mechanisms to maintain data consistency

Key Features:
- Decentralization: No single point of control
- Immutability: Data cannot be altered once recorded
- Transparency: All participants can see the data
- Security: Cryptographic protection of data
- Consensus: Agreement on data validity across participants

Types of Distributed Ledgers:
- Blockchain: Data stored in blocks linked by cryptographic hashes
- Directed Acyclic Graph (DAG): Data stored in a graph structure
- Hashgraph: Uses virtual voting for consensus
- Holochain: Agent-centric distributed ledger

Benefits:
- Reduced costs: Eliminates intermediaries and middlemen
- Increased speed: Direct peer-to-peer transactions
- Enhanced security: Cryptographic protection and consensus
- Improved transparency: All participants see the same data
- Greater resilience: No single point of failure

Use Cases:
- Financial services: Cross-border payments, trade finance
- Supply chain: Product tracking and verification
- Healthcare: Patient data sharing and management
- Government: Public records and voting systems
- Real estate: Property ownership and transfer records
""",

    "proof_of_work": """
Proof of Work (PoW) is a consensus mechanism used in blockchain networks to validate transactions and create new blocks:

What is Proof of Work:
- A consensus algorithm that requires computational work to validate transactions
- Miners compete to solve complex mathematical puzzles
- The first miner to solve the puzzle gets to add the next block
- Requires significant computational power and energy consumption
- Provides security through economic incentives

How Proof of Work Works:
1. Transactions are collected into a block
2. Miners compete to solve a cryptographic puzzle
3. The puzzle requires finding a hash that meets certain criteria
4. The first miner to find the solution broadcasts it to the network
5. Other nodes verify the solution and add the block to the chain
6. The successful miner receives a reward (block reward + transaction fees)

Key Characteristics:
- Energy Intensive: Requires significant computational power
- Secure: Difficult to attack due to high energy costs
- Decentralized: Anyone can participate in mining
- Transparent: All mining activity is visible
- Immutable: Changing past blocks requires redoing all work

Advantages:
- High security: Expensive to attack the network
- Decentralized: No single point of control
- Proven: Bitcoin has been secure for over a decade
- Transparent: All mining activity is visible
- Censorship resistant: Difficult to stop transactions

Disadvantages:
- High energy consumption: Significant environmental impact
- Slow transactions: Limited throughput and high fees
- Centralization risk: Mining pools can concentrate power
- Wasteful: Most computational work is discarded
- Scalability issues: Difficult to scale to high transaction volumes

Examples:
- Bitcoin: The first and most well-known PoW blockchain
- Ethereum (before merge): Used PoW before switching to PoS
- Litecoin: Uses a different hash function than Bitcoin
- Dogecoin: Based on Litecoin's PoW implementation
""",

    "sui_blockchain_type": """
Sui is a Layer 1 blockchain that uses a unique consensus mechanism and object-centric model:

Sui Blockchain Type:
- Layer 1 Blockchain: Base layer for applications and smart contracts
- Public Blockchain: Open to anyone, permissionless
- Smart Contract Platform: Supports decentralized applications
- Object-Centric: Uses objects instead of accounts
- High Performance: Designed for scalability and speed

Sui's Consensus Mechanism:
- Narwhal and Bullshark: Sui's consensus algorithm
- Not Proof of Work: Uses a more efficient consensus
- Not Proof of Stake: Uses a different approach
- Byzantine Fault Tolerant: Can handle malicious nodes
- High Throughput: Can process thousands of transactions per second

Sui's Unique Features:
- Object-Centric Model: Everything is an object with unique ID
- Parallel Execution: Transactions on different objects can run simultaneously
- Move Language: Custom programming language for smart contracts
- Horizontal Scalability: Performance improves with more validators
- Sub-second Finality: Transactions are finalized quickly

Sui vs Other Blockchains:
- vs Bitcoin: Much faster, supports smart contracts, uses objects
- vs Ethereum: Faster, more scalable, object-centric model
- vs Solana: Different consensus mechanism, object-centric
- vs Avalanche: Different architecture, Move language

Sui's Architecture:
- Validators: Maintain the network and process transactions
- Objects: The fundamental data structures
- Transactions: Operations that modify objects
- Consensus: Narwhal and Bullshark for agreement
- Storage: Efficient object storage and retrieval

Sui's Advantages:
- High Performance: Fast transaction processing
- Low Fees: Cost-effective transactions
- Developer Friendly: Easy to build applications
- Scalable: Can handle high transaction volumes
- Secure: Built with security in mind
""",

    "blockchain_consensus": """
Consensus mechanisms are the methods by which blockchain networks agree on the state of the ledger:

What is Consensus:
- A method for network participants to agree on the validity of transactions
- Ensures all nodes have the same version of the blockchain
- Prevents double-spending and maintains network security
- Determines which transactions are valid and which blocks to add
- Establishes trust in a decentralized system

Types of Consensus Mechanisms:

Proof of Work (PoW):
- Miners compete to solve cryptographic puzzles
- Requires significant computational power
- Used by Bitcoin and Ethereum (before merge)
- High security but energy intensive

Proof of Stake (PoS):
- Validators are chosen based on stake (coins held)
- More energy efficient than PoW
- Used by Ethereum 2.0, Cardano, Polkadot
- Lower energy consumption but potential centralization

Delegated Proof of Stake (DPoS):
- Token holders vote for delegates to validate transactions
- Faster than traditional PoS
- Used by EOS, Tron, Steem
- More centralized but higher performance

Proof of Authority (PoA):
- Validators are pre-approved and known entities
- Used in private and consortium blockchains
- High performance but less decentralized
- Examples: VeChain, Binance Smart Chain

Byzantine Fault Tolerance (BFT):
- Can handle up to 1/3 malicious nodes
- Used by Sui, Algorand, Cosmos
- Fast finality and high security
- Requires known validator set

Consensus Requirements:
- Agreement: All honest nodes agree on the same state
- Validity: Only valid transactions are included
- Termination: All honest nodes eventually decide
- Integrity: No honest node can be forced to accept invalid data
- Liveness: The system continues to make progress

Consensus Trade-offs:
- Security vs Performance: Higher security often means lower performance
- Decentralization vs Efficiency: More decentralized systems are often slower
- Energy vs Speed: PoW is secure but energy intensive
- Trust vs Speed: More trusted systems can be faster
""",

    "blockchain_security": """
Blockchain security refers to the measures and mechanisms that protect blockchain networks from attacks and ensure data integrity:

Blockchain Security Features:
- Cryptographic Hashing: SHA-256, Keccak-256 protect data integrity
- Digital Signatures: Verify transaction authenticity and ownership
- Consensus Mechanisms: Prevent malicious actors from controlling the network
- Immutability: Data cannot be altered once recorded
- Decentralization: No single point of failure

Common Security Threats:
- 51% Attacks: When a single entity controls majority of network power
- Double Spending: Spending the same cryptocurrency twice
- Sybil Attacks: Creating multiple fake identities
- Eclipse Attacks: Isolating nodes from the network
- Smart Contract Vulnerabilities: Bugs in smart contract code

Security Measures:
- Multi-signature: Require multiple signatures for transactions
- Time Locks: Delay transaction execution
- Hash Functions: Cryptographically secure hashing algorithms
- Merkle Trees: Efficient verification of data integrity
- Zero-Knowledge Proofs: Prove knowledge without revealing information

Blockchain Security Best Practices:
- Private Key Management: Secure storage of private keys
- Multi-signature Wallets: Require multiple approvals
- Regular Updates: Keep software and protocols updated
- Code Audits: Review smart contract code for vulnerabilities
- Network Monitoring: Monitor for suspicious activity

Security in Different Blockchains:
- Bitcoin: High security through PoW and decentralization
- Ethereum: Smart contract security and network protection
- Sui: Object-centric security and Move language safety
- Private Blockchains: Access control and permission management
- Consortium Blockchains: Multi-party security and governance
"""
}