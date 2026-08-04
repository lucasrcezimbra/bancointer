Low-level API
==============

API
---

.. automodule:: inter
   :members: Client, Scopes
   :undoc-members:
   :show-inheritance:


Testing
-------

Use :class:`inter.testing.ClientFake` when you need the low-level client shape
without network or certificates. Override ``balance``, ``statements``, or
``pay_barcode_data`` on the instance.

Example::

    from inter.testing import ClientFake

    client = ClientFake()
    client.balance = {"disponivel": 42.5}
    assert client.get_balance() == {"disponivel": 42.5}

.. automodule:: inter.testing
   :members: ClientFake
   :undoc-members:
   :show-inheritance:
