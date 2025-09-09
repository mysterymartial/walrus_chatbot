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
}