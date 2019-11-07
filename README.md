# QC16 Base Station project

## Overview
This project acts as a visual "bank" for the Queercon16 badge game. Users in the game generate currencies through
participating in various missions on their individual badges, both electronic and non-electronic. As they continue to
 earn the various currency, they can contribute their currency towards the Queercon kickstarter which powers up the
 pillars found throughout the venue.

## Design

The design of this project consist of two major components: a Python application and a React Application. The python
application managed handling the serial connections of the badges along with interfacing with the pillars and
uploading the results to AWS. The React application was handled working with the UI displaying the latest
contributions and overall results.

### Python Application

Consists of two components:

- Message Ingestion
- Message Processor

#### Message Ingestion

In order to communciate with badges, a serial connection is established along with a protocol handshake which the
badges use to ensure a currency dump does not happen accidentally without counting towards the overall goal. There is
 a process manager which is running and opens new serial ports when a USB to RJ12 adaptor is plugged into the
 Raspberry Pi. After the port is opened and a badge successfully connects, a state machine handles the message dump
 and then converts the message into an internal format before dumping into a message queue, allowing for multiple
 simultaneous badge connections at a time while guaranteeing all messages get processed in the order they were
 received.

#### Message Processor

The message processor consumes from the aforementioned message queue which fires a message being sent to the
connected LED pillar before sending the message to be written to the AWS managed DB.

### React Application

The React application is using the `create-react-app` template as the starting point for the project and builds on
top of it by having two async-await calls to get the aggregate results for the various currencies as they are stored
in AWS.

The entirety of this portion of the project was authored by [@gbps](https://github.com/Gbps) and couldn't have been
done without him.

# Contributors

Special thanks goes out to the following:

[@gbps](https://github.com/Gbps)
[@duplico](https://github.com/duplico)
