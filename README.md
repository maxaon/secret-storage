# Secret Storage 
This is prototype of the SPA. 
Main porpoise of this project is to create framework for applications with client-side encryption 
and verification of server responses.
 
## How it works 

For the user:

1. Generate PGP private key
2. Import key: public part will be copied to the server, private armored part will be kept in browser
3. When user firstly access to the encrypted data, passphrase will be asked, and data will be using private key.
4. When user changes something, app will encrypt and sign data snd store on the server.
 
Unencrypted data will not be stored or transferred to the server.

### Additional security 
To minimize risks additional methods should be used:

1. HTTPS
2. CSP with signature. 
3. All cryptography should be made outside of the app in the extension.


### CSP with signature  
Method guarantee integrity of the source code (JS, CSS etc)
How it works:

1. Developer verifies all the source code.
2. Creating minified version of the source files and calculating their sha256 hashes.
3. Creating valid CSP header. For example, `Content-Security-Policy: script-src 'sha256-HASH'`. 
4. Signing resulting string whit private key. 
5. CSP header and signature transfers to the server, and server always send them to the client.

Verification

1. Browser extension on protected page verify each request.
2. When headers are received extension validate provided signature.
3. If no signature is present or signature is not verified extension aborts request and show message.

Running demo of the dev branch:  [http://demo.sunset.dp.ua](http://demo.sunset.dp.ua/)

## Project status  
This is early dev demo version

                                           


