#!/usr/bin/env python3

from pybytom.script import script_hash, p2wsh_address
from equity import Equity

from ..config import bytom

# Bytom configuration
bytom = bytom()

# Hash Time Lock Contract (HTLC) Script
HTLC_SCRIPT = """
contract HTLC (
  secret_hash: Hash,
  recipient: PublicKey,
  sender: PublicKey,
  sequence: Integer
) locks valueAmount of valueAsset {
  clause claim(preimage: String, sig: Signature) {
    verify sha256(preimage) == secret_hash
    verify checkTxSig(recipient, sig)
    unlock valueAmount of valueAsset
  }
  clause refund(sig: Signature) {
    verify above(sequence)
    verify checkTxSig(sender, sig)
    unlock valueAmount of valueAsset
  }
}
"""


# Hash Time Lock Contract
class HTLC:
    """
    Bytom Hash Time Lock Contract (HTLC) class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns:  HTLC -- Bytom HTLC instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    # Initialization
    def __init__(self, network="testnet"):
        # Bytom network.
        self.network = network
        # Initializing equity
        self.equity = None

    # Initialize new HTLC Contract script
    def init(self, secret_hash, recipient_public, sender_public, sequence=bytom["sequence"]):
        """
        Initialize Bytom Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: str
        :param recipient_public: Bytom recipient public key.
        :type recipient_public: str
        :param sender_public: Bytom sender public key.
        :type sender_public: str
        :param sequence: Bytom sequence number of expiration block, defaults to Bytom config sequence (15).
        :type sequence: int
        :returns: HTLC -- Bytom Hash Time Lock Contract (HTLC) instance.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        <shuttle.providers.bytom.htlc.HTLC object at 0x0409DAF0>
        """

        # Checking parameters
        if not isinstance(secret_hash, str):
            raise TypeError("secret hash must be string format")
        if len(secret_hash) != 64:
            raise ValueError("invalid secret hash, length must be 64.")
        if not isinstance(recipient_public, str):
            raise TypeError("recipient public key must be string format")
        if len(recipient_public) != 64:
            raise ValueError("invalid recipient public key, length must be 64.")
        if not isinstance(sender_public, str):
            raise TypeError("sender public key must be string format")
        if len(sender_public) != 64:
            raise ValueError("invalid sender public key, length must be 64.")
        if not isinstance(sequence, int):
            raise TypeError("sequence must be integer format")

        # HTLC agreements
        HTLC_AGREEMENTS = [
            secret_hash,  # secret_hash: Hash
            recipient_public,  # recipient: PublicKey
            sender_public,  # sender: PublicKey
            sequence,  # sequence: Integer
        ]
        # Compiling HTLC contract
        self.equity = Equity(bytom[self.network]["bytom"])\
            .compile_source(HTLC_SCRIPT, HTLC_AGREEMENTS)
        return self

    # Bytom HTLC from bytecode
    def from_bytecode(self, bytecode):
        self.equity = dict(program=bytecode)
        return self

    # Bytecode HTLC script
    def bytecode(self):
        """
        Get Bytom htlc bytecode.

        :returns: str -- Bytom Hash Time Lock Contract (HTLC) bytecode.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        >>> htlc.bytecode()
        "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        """

        if not self.equity or "program" not in self.equity:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.equity["program"]

    # OP Code of HTLC script
    def opcode(self):
        """
        Get Bytom htlc opcode.

        :returns: str -- Bytom Hash Time Lock Contract (HTLC) opcode.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        >>> htlc.opcode()
        "0x64 0x91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 0xac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 0x2b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff DEPTH 0x547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac FALSE CHECKPREDICATE"
        """

        if not self.equity or "opcodes" not in self.equity:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.equity["opcodes"]

    # HTLC script hash
    def hash(self):
        """
        Get Bytom Hash Time Lock Contract (HTLC) hash.

        :returns: str -- Bytom Hash Time Lock Contract (HTLC) hash.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        >>> htlc.hash()
        "b3c67ffb38fa981ee368aa9dfc856bd62c6b93df9069deccd8159911c46c216a"
        """

        if not self.equity or "opcodes" not in self.equity:
            raise ValueError("htlc script is none, initialization htlc first")
        return script_hash(bytecode=self.bytecode())

    # HTLC script address
    def address(self):
        """
        Get Bytom Hash Time Lock Contract (HTLC) address.

        :returns: str -- Bytom Hash Time Lock Contract (HTLC) address.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        >>> htlc.address()
        "bm1qk0r8l7ecl2vpacmg42wleptt6ckxhy7ljp5aanxczkv3r3rvy94q4a2zpc"
        """

        if not self.equity or "opcodes" not in self.equity:
            raise ValueError("htlc script is none, initialization htlc first")
        return p2wsh_address(script_hash=script_hash(bytecode=self.bytecode()), network=self.network)
