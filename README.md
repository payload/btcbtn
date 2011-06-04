== btcbtn

* a website with a bitcoin button which enables you to donate some bitcoins
  with one click
* the user has to have the btcbtn server running
* this button links to a client side local url like:

    http://localhost:8170/donate/0.1BTC/{address}

* a locally running server has access to the wallet and will push these bitcoins
  to the address after some confirmation
* you don't need to push your bitcoins to a remote wallet in advance!
* put this link or the code for the button on your website and substitute
  at least {address} with your bitcoin address, change also the amount if you
  like

    <a href="http://localhost:8170/donate/0.1BTC/{address}">
      donate 0.1 BTC
    </a>

=== architecture

* python and its batteries

* listen on localhost:8170
* show confirmation site on HTTP GET /donate/(\d+(.\d+)?)BTC/[0-9a-zA-Z]+
* donate on confirmation
* to donate, call bitcoin sendtoaddress SOME-BITCOIN-ADDRESS AMOUNT

* the confirmation site must contain localhost specific information which are
  secret to the outside world so click fraud can be detected
* you can see it in the url, but some browsers dont show it
* if this is not possible, pop up a windows independant of the browser

