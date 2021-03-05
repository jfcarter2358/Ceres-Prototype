```
   ________
  /        |
 /   ______|
|   /
|  |        ___  __  __ ___  ___
|   \______/ _ \|  |/__/ _ \/  _|
 \         | __/|   /  | __/\_  \
  \________\____|__|   \____|___/
```
## About
Ceres is a database system designed to allow for quick retrieval of log messages. It was designed for use with the Whitetail log viewer after exising database solutions proved to be too slow.

### Naming
Ceres is named after the Roman goddess of agriculture for the way in which the system "harvests" data from the files it is stored on

## How It Works
** WIP **

## Note
The Ceres prototype is a "first pass" at building the system in a language that allows for quick and easy iteration (Python).  This will be ported over to a better suited language (i.e. Rust) in the future.

## To Do
- [x] Delete data from database
- [x] Non-logical operators
    - [x] LIMIT operation
    - [x] ORDERBY operation
    - [x] ORDERDESC operation
- [ ] Batch read
- [x] Read configuration from file
- [ ] Be able to access log by ID
- [x] Recover "free data" object on start from existing data
- [ ] Schema validation
- [x] Query validation

## Contact
This software is written by John Carter. If you have any qeustions or concers feel free to create an issue on GitHub or send me an email at jfcarter2358(at)gmail.com