High-level API
==============

API
---

.. automodule:: inter
   :members: Inter, Operation, Payment
   :undoc-members:
   :show-inheritance:


Testing
-------

Use :class:`inter.testing.InterFake` in unit tests so you do not call the live
Banco Inter API. Override ``balance``, ``statement``, or ``pay_barcode_data``
to control return values.

Example::

    from decimal import Decimal
    from inter.testing import InterFake

    inter = InterFake()
    inter.balance = Decimal("1000.00")
    assert inter.get_balance() == Decimal("1000.00")

.. automodule:: inter.testing
   :members: InterFake
   :undoc-members:
   :show-inheritance:
