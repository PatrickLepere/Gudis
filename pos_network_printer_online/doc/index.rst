==========================
POS NETWORK PRINTER ONLINE
==========================

Installation
============

* Copy the modules in addons path and install it from Apps menu
* Uncomment depends in ``pos_network_printer`` in __manifest__.py file of the module

Configuration
=============

* Open menu ``Point Of Sale >>  Configuration >> Printer Connector``
* Create Printer Connector :
    * Click Create
    * Specify name
    * Click Save
* Open menu ``Point Of Sale >>  Configuration >> Network Printer``
* Edit selected network printer :
    * Specify **Printer Connector** box
    * Click save
* Open menu ``Point Of Sale >>  Configuration >> Point of Sale`` at **Bill & Receipts** section
* Keep Ticket print mode to Network
* Odoo Printer Connector:
    * Extract from zip directory in the module to printer in local network
    * Configure printer.conf (host, port, dbname, user, password, token)
    * Execute connector.exe

Usage
=====

* Print ticket from Point Of Sale
* Open menu ``Point Of Sale >>  Configuration >> Queue print`` to see queue print
* Odoo Printer Connector will print receipt in local printer


