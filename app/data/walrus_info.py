# ======================
# app/data/walrus_info.py
# ======================

WALRUS_INFO = {
    "what_is_walrus": """
Walrus is a data availability (DA) solution built specifically for the Sui blockchain. It provides a decentralized, scalable, and efficient way to store and retrieve data for Sui applications.

Key Features:
- Data Availability: Ensures data is accessible and verifiable across the network
- Blob Storage: Stores large data objects (blobs) efficiently
- Sui Integration: Native integration with Sui's object-centric model
- Decentralized: Distributed storage across multiple nodes
- Cost-Effective: Optimized for Sui's gas model and storage requirements

Walrus enables developers to store large files, media, and other data types that would be too expensive to store directly on-chain, while maintaining the security and decentralization benefits of blockchain technology.
""",

    "walrus_da": """
Walrus Data Availability (DA) is a core component that ensures data stored in the Walrus network remains accessible and verifiable. 

How it works:
- Data is split into chunks and distributed across multiple nodes
- Cryptographic proofs ensure data integrity
- Redundancy prevents data loss
- Fast retrieval through optimized indexing

Benefits for Sui:
- Reduces on-chain storage costs
- Enables large file storage for dApps
- Maintains data availability guarantees
- Integrates with Sui's object model
""",

    "walrus_blobs": """
Walrus Blobs are the fundamental storage units in the Walrus network. A blob is a large data object that can contain any type of data - files, media, documents, or application data.

Blob Characteristics:
- Size: Can store large files (up to several GB)
- Immutable: Once stored, blobs cannot be modified
- Addressable: Each blob has a unique identifier
- Verifiable: Cryptographic proofs ensure integrity
- Retrievable: Fast access through distributed network

Use Cases:
- NFT metadata and media
- Game assets and resources
- Document storage
- Media files for dApps
- Large datasets for analytics

Blobs are essential for applications that need to store data off-chain while maintaining blockchain security guarantees.
""",

    "walrus_architecture": """
Walrus Architecture is designed for high performance, scalability, and integration with Sui:

Core Components:
- Storage Nodes: Distributed nodes that store blob data
- Index Nodes: Maintain metadata and enable fast retrieval
- Validator Nodes: Ensure data integrity and availability
- Gateway Nodes: Handle client requests and data routing

Key Design Principles:
- Decentralized: No single point of failure
- Scalable: Horizontal scaling as network grows
- Efficient: Optimized for Sui's gas model
- Secure: Cryptographic proofs and redundancy
- Fast: Sub-second data retrieval

Integration with Sui:
- Native object references in Sui transactions
- Gas-efficient data storage
- Seamless developer experience
- Object-centric data model compatibility
""",

    "walrus_token": """
Walrus Token (WAL) is the native utility token of the Walrus network:

Token Economics:
- Utility: Used for storage fees, node rewards, and governance
- Supply: Deflationary model with burning mechanisms
- Staking: Token holders can stake to earn rewards
- Governance: WAL holders participate in network decisions

Current Price: Available via CoinGecko API integration
Market Cap: Varies based on network adoption
Use Cases:
- Pay for data storage and retrieval
- Stake for network security
- Participate in governance votes
- Earn rewards for providing storage

The token ensures the economic sustainability of the Walrus network while aligning incentives between users, developers, and node operators.
""",

    "walrus_sui": """
Walrus on Sui represents a perfect integration between decentralized storage and blockchain technology:

Integration Benefits:
- Object-Centric: Leverages Sui's object model for efficient data references
- Gas Efficiency: Reduces on-chain storage costs significantly
- Developer Experience: Simple APIs for storing and retrieving data
- Scalability: Enables applications with large data requirements

Technical Integration:
- Sui Objects: Store blob references as Sui objects
- Transaction Integration: Include blob operations in Sui transactions
- Smart Contracts: Access blob data from Move smart contracts
- Wallet Integration: Seamless user experience

Use Cases on Sui:
- Gaming: Store game assets and user progress
- NFTs: Large media files for NFT collections
- DeFi: Store complex financial data and analytics
- Social: User-generated content and media
- Enterprise: Document storage and collaboration

This integration makes Sui the ideal blockchain for applications requiring both smart contract functionality and large-scale data storage.
""",

    "walrus_validators": """
Walrus Network Validators are the core infrastructure providers that maintain the Walrus data availability network:

What are Validators:
- Validators are nodes that store and serve blob data across the Walrus network
- They participate in consensus for data availability and integrity
- Validators maintain network security and decentralization
- They earn rewards for providing storage services to the network

Validator Functions:
- Store and serve blob data across the network
- Participate in consensus for data availability
- Maintain network security and decentralization
- Earn rewards for providing storage services
- Ensure data redundancy and fault tolerance

Network Statistics:
- Validator count varies based on network growth and adoption
- Validators are distributed globally for optimal performance
- Each validator maintains redundant copies of blob data
- Network scales horizontally as more validators join
- Current validator count and network stats available via Walrus Scan
- For exact validator count, check walrusscan.com for real-time data
- Validator numbers change as the network grows and new validators join

Validator Requirements:
- Sufficient storage capacity for blob data
- Reliable network connectivity
- Stake WAL tokens for network participation
- Meet technical requirements for data serving
- Maintain uptime and data availability

Real-time network statistics including validator count, total stake, and network health metrics are available through Walrus Scan APIs at walrusscan.com.
""",

    "walrus_epochs": """
Walrus Epochs are time-based periods that govern the network's operation and validator rotation:

What are Walrus Epochs:
- Epochs are fixed time periods (14 days) that define network cycles
- Each epoch has a specific set of active validators
- Epochs ensure network decentralization through validator rotation
- Epoch boundaries trigger validator set updates and reward distributions

Epoch Duration:
- Standard Duration: 14 days per epoch
- Epoch Length: 14 days = 336 hours = 20,160 minutes = 1,209,600 seconds
- Epoch Cycle: Continuous 14-day periods with no gaps
- Time Zone: Epochs are typically based on UTC time
- Consistency: All epochs have the same duration for predictability

Epoch Functions:
- Validator Set Management: Determines which validators are active in each epoch
- Reward Distribution: Validators receive rewards at epoch boundaries
- Network Security: Regular validator rotation prevents centralization
- Consensus Updates: Network parameters can be updated at epoch boundaries
- Blob Storage: Epochs track blob storage periods and data availability

Epoch Lifecycle:
- Epoch Start: New validator set becomes active
- Epoch Progress: Validators process blob storage requests
- Epoch End: Rewards distributed, validator set updated
- Epoch Transition: Smooth handover to next epoch's validators

Epoch Information:
- Current epoch number and remaining time
- Active validators for current epoch
- Epoch rewards and stake distribution
- Historical epoch data and statistics
- Epoch-based network performance metrics

Real-time epoch information is available through Walrus Scan APIs, showing current epoch, remaining time, and validator details.
""",

    "walrus_blob_ids": """
Walrus Blob IDs are unique identifiers for data blobs stored on the Walrus network:

What are Blob IDs:
- Blob IDs are cryptographic hashes that uniquely identify each blob
- Generated using content-addressed storage (CAS) principles
- Immutable identifiers that cannot be changed or duplicated
- Used for blob retrieval, verification, and reference

Blob ID Characteristics:
- Unique: Each blob has a distinct, non-reversible identifier
- Content-based: ID is derived from blob content using cryptographic hashing
- Immutable: Blob ID remains constant as long as content is unchanged
- Verifiable: Can be used to verify blob integrity and authenticity

Blob ID Usage:
- Storage: Blob IDs are used to store and organize blob data
- Retrieval: Used to locate and fetch specific blobs from the network
- Verification: Enable integrity checks and content validation
- Reference: Allow other systems to reference specific blob data
- Tracking: Monitor blob access, usage, and lifecycle

Blob ID Format:
- Typically 32-byte (256-bit) cryptographic hashes
- Often represented as hexadecimal strings
- Compatible with standard hash functions (SHA-256, Blake3)
- Designed for efficient storage and transmission

Blob ID Management:
- Generated automatically when blobs are created
- Stored in distributed index across validator nodes
- Used for efficient blob discovery and retrieval
- Enable content deduplication and optimization
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

    "walrus_storage_costs": """
Walrus Storage Costs and Pricing:

Storage Pricing Model:
- Pay-per-use: Users pay for actual storage consumed
- Epoch-based billing: Costs calculated per 14-day epoch
- Blob size pricing: Costs scale with data size stored
- Network demand pricing: Dynamic pricing based on network usage
- Validator rewards: Storage fees distributed to validators

Cost Factors:
- Data Size: Larger blobs cost more to store
- Duration: Longer storage periods increase costs
- Network Congestion: Higher demand increases prices
- Validator Count: More validators can reduce costs
- Storage Redundancy: Multiple copies increase costs

Pricing Structure:
- Base Rate: Minimum cost per MB stored per epoch
- Volume Discounts: Reduced rates for large storage amounts
- Long-term Storage: Discounts for extended storage periods
- Network Fees: Additional fees for data retrieval and access
- Validator Fees: Portion of fees goes to network validators

Economic Benefits:
- Cost-effective: Cheaper than on-chain storage
- Scalable: Costs scale with usage
- Predictable: Transparent pricing model
- Efficient: Optimized for Sui's gas model
- Decentralized: No single point of pricing control

Storage Cost Examples:
- Small files (< 1MB): Minimal cost per epoch
- Medium files (1-10MB): Moderate cost per epoch
- Large files (> 10MB): Higher cost but still cost-effective
- Bulk storage: Volume discounts available
- Long-term storage: Reduced rates for extended periods

Current Pricing Information:
- Real-time pricing varies based on network conditions and demand
- For current storage costs per epoch, check Walrus Scan APIs
- Pricing is dynamic and updated based on network usage
- Official pricing information is available through Walrus Labs documentation
- Network statistics and current rates can be found at walrusscan.com
""",

    "walrus_economics": """
Walrus Network Economics:

Economic Model:
- Token-based: Uses WAL tokens for all economic activities
- Fee-based: Revenue generated through storage and access fees
- Validator rewards: Validators earn tokens for providing services
- Network incentives: Economic rewards encourage participation
- Deflationary: Token burn mechanisms reduce supply over time

Revenue Streams:
- Storage Fees: Primary revenue from blob storage
- Access Fees: Revenue from data retrieval and access
- Network Fees: Transaction fees for network operations
- Validator Fees: Portion of all fees goes to validators
- Premium Services: Additional fees for enhanced features

Cost Structure:
- Storage Costs: Pay-per-use model for blob storage
- Network Costs: Fees for data transmission and access
- Validator Costs: Staking requirements and operational costs
- Development Costs: Ongoing network development and maintenance
- Security Costs: Network security and consensus mechanisms

Economic Incentives:
- Validator Rewards: Earn tokens for providing storage services
- Staking Rewards: Earn rewards for staking WAL tokens
- Network Participation: Incentives for running nodes and validators
- Data Availability: Rewards for ensuring data accessibility
- Network Growth: Incentives for expanding network capacity

Token Utility:
- Storage Payments: Required for storing data on Walrus
- Validator Staking: Must stake tokens to become a validator
- Governance: Vote on network proposals and changes
- Network Fees: Pay for network operations and access
- Economic Security: Token value secures the network

Economic Benefits:
- Cost Efficiency: Lower costs than traditional storage
- Scalability: Economic model scales with network growth
- Decentralization: No single entity controls pricing
- Transparency: All economic activities are on-chain
- Sustainability: Long-term economic viability

Real-time economic data including token prices, network fees, and validator rewards is available through Walrus Scan APIs.
"""
}
