Wireless Attendance
===================

A Python package for rapid club meeting attendance via reading Northeastern University Husky Cards.

Installing
----------

It is recommended that you first create a virtual environment before installing this package and its dependencies. For more information about creating a virtual environment, see the `Python Documentation for the venv module`_. This package supports Python 3.5 or greater.

Install the latest and greatest from git by executing

.. code-block:: console

    $ pip install git+https://github.com/NEUWireless/Wireless-Attendance

.. _Python Documentation for the venv module: https://docs.python.org/3.6/library/venv.html

Configuration the Google API
----------------------------

You will need credentials for a Google Service Account to interface with the Google Sheets backend. For instructions to get OAuth2 credentials, see the `gspread documentation`_.

Make sure that you have the Sheets API enabled.

Once you have a service account ready, create a new Google Sheet and share it with the service account.

Testing the Google Sheets Backend
---------------------------------

To test the connection with Google Sheets, execute

.. code-block:: console

    $ python3 -m wireless_attendance -mock-reader --spreadsheet-url URL

where ``URL`` is the complete URL to the spreadsheet your created earlier. You may alternative access the sheet via its name or ID, as discussed below.

This will open a connection to the Sheets API using the credentials file ``wireless-attendance-credentials.json`` located in the current working directory. If you would like to use a credentials file located elsewhere, pass ``--credentials-file CRED_FILE.json`` to the command above.

You may receive some errors due to certain APIs not being enabled or not having permissions for the sheet. Make sure that the service account has edit permissions on the target sheet and the the correct APIs are enabled for your account.

If all goes well, you should be prompt to enter mock card IDs. Enter a few values and make sure that they are populated into the spreadsheet.

.. _gspread documentation: https://gspread.readthedocs.io/en/latest/oauth2.html

Running
-------

.. code-block:: shell

    $ python3 -m wireless_attendance --help
    usage: wireless_attendance [-h] [--credentials-file CREDENTIALS_FILE]
                               (--spreadsheet-id SPREADSHEET_ID | --spreadsheet-name SPREADSHEET_NAME | --spreadsheet-url SPREADSHEET_URL | -no-sheet)
                               [-mock-reader]

    Wireless Attendance Tracking

    optional arguments:
      -h, --help            show this help message and exit
      --credentials-file CREDENTIALS_FILE
                            The path to the Google Service Account credentials.
                            See the gspread documentation for information on how
                            to obtain a credentials file:
                            https://gspread.readthedocs.io/en/latest/oauth2.html
      --spreadsheet-id SPREADSHEET_ID
                            The ID of the spreadsheet to store attendance data.
      --spreadsheet-name SPREADSHEET_NAME
                            The name of the spreadsheet to store attendance data.
      --spreadsheet-url SPREADSHEET_URL
                            The complete URL to the spreadsheet to store
                            attendance data.
      -no-sheet             If specified, the process will not attempt to connect
                            to the Google Sheets API. All card reads will still be
                            written the the logger.
      -mock-reader          If specified, the process will not attempt to access
                            the card reader. Mock UUIDs will be read from stdin.


License
-------

This software is licensed under the `MIT License`_. For more
information, read the file `LICENSE`_.

.. _MIT License: https://opensource.org/licenses/MIT
.. _LICENSE: ./LICENSE
