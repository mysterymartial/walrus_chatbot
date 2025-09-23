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

Validator Role:
- Store and serve blob data across the network
- Participate in consensus for data availability
- Maintain network security and decentralization
- Earn rewards for providing storage services

Network Statistics:
- Validator count varies based on network growth and adoption
- Validators are distributed globally for optimal performance
- Each validator maintains redundant copies of blob data
- Network scales horizontally as more validators join

Validator Requirements:
- Sufficient storage capacity for blob data
- Reliable network connectivity
- Stake WAL tokens for network participation
- Meet technical requirements for data serving

Current network stats are available through Walrus Scan APIs, showing real-time validator count, total stake, and network health metrics.
"""
}
