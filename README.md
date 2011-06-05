# btcbtn

* today bitcoin enabled websites have a line with a bitcoin address so you
  can copy and paste it to donate some bitcoins
* btcbtn is a system to switch this copy paste line into a button so you need
  only (at the time) 2 clicks to donate an amount of bitcoins
* you don't need to register with a third service where you put your bitcoins
  into a remote wallet
* unfortunatly the client side needs this software running in the background
  and `bitcoin` in the `PATH` when running `btcbtn` or provide the path to
  your bitcoin executable as an argument

  ```sh
  btcbtn [--bitcoin=<PATH TO BITCOIN>] [--daemon]
  ```

* quit btcbtn with `killall btcbtn` when you called it as a daemon :P

## the button

* put this link or the code for the button on your website and substitute
  at least the bitcoin address with your bitcoin address
* change also the amount if you like in both places

    ```html
    <a href="http://localhost:8170/donate/12UjAGVyKwmH3dN7TmEvxGLf3iomNX8G43?amount=0.1">
      donate 0.1 BTC
    </a>
    ```

* the same a little bit styled
    ```html
    <div class="btcbtn"
        style="
            display: inline-block;
            margin: 0.1em;
            padding: 0.5em;
            -khtml-border-radius: 0.3em;
            -moz-border-radius: 0.3em;
            -webkit-border-radius: 0.3em;
            border-radius: 0.3em;
            background-color: #CCFF55;
        ">
        <a href="http://localhost:8170/donate/12UjAGVyKwmH3dN7TmEvxGLf3iomNX8G43?amount=0.1">
            donate 0.1 BTC
        </a>
    </div<
    ```

## architecture

* it uses python and its batteries

* listen on `localhost:8170`
* show confirmation site on `HTTP GET /donate/[0-9a-zA-Z]+?amount=(\d+(.\d+)?)`
  which has a link to the confirmation
* donate on confirmation
* to donate, call `bitcoin sendtoaddress ADDRESS AMOUNT`

## future plans

* fraud prevention for browsers which don't show the url line
* a styled button
* integration with `bitcoin`
* client side change of the amount
* donate with latency so you can revoke a donation and dont need a confirmation
  ultimately resulting in 1-click bitcoin transfer

