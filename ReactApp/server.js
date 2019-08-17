/******************************************************************************
 *    Author: Michael Frohlich
 *      Date: 2019
 * Copyright: 2019 Michael Frohlich - Modified BSD License
 *****************************************************************************/

config = {
    mysqlport: '3306',
    mysqlhost: 'qc16-test-db-1.cywp7i1l4mst.us-west-2.rds.amazonaws.com',
    dbname: 'qc16_db_test_1',
    table_name: 'badge_messages',
    user: 'admin',
    password: 'qc_16_db',
    webport: 8090
};

const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const mysql = require('mysql');
const cors = require('cors');

app.use(cors());

const conn = mysql.createConnection({
    host: config.mysqlhost,
    port: config.mysqlport,
    user: config.user,
    password: config.password,
    database: config.dbname
});

console.log("Connecting to mysql...");
conn.connect();
console.log("Connected.");

app.use(express.static(path.join(__dirname, 'build')));

// get the total amount of currency and call a callback when data is available
function getTotalCurrency(badgeType, currencyType, callback) {
    const query = conn.query(`SELECT SUM(quantity) FROM \`${config.table_name}\` WHERE badge_type=? AND currency_type=?`, [
        badgeType, currencyType
    ], function(error, results, fields) {
        if (error) throw error;

        // copy result object from mysql
        let res = JSON.parse(JSON.stringify(results));

        // grab the result object we're interested in
        res = res[0]['SUM(quantity)'];

        // call our callback
        callback(res || 0)
    });
    return 'done';
}

// get the recent badges that made a donation to two different types
function getRecents(cType1, cType2, limit, callback) {
    const query = conn.query(`SELECT badge_id, badge_type, currency_type, quantity FROM \`${config.table_name}\` WHERE (currency_type=? OR currency_type=?) AND NOT quantity=0 ORDER BY creation_time DESC LIMIT ${limit}`, [
        cType1, cType2, limit
    ], function(error, results, fields) {
        if (error) throw error;

        // copy result object from mysql
        let res = JSON.stringify(results);

        // call our callback
        callback(res)
    })
    return 'done';
}

// access /getTotal/badgeType/currencyType to get the amount
app.get('/getTotal/:badgeType/:currencyType/', function(req, res) {
    console.log(req.params);
    getTotalCurrency(req.params.badgeType, req.params.currencyType, (r) => {
        return res.send(r.toString());
    })
});

// access /getTotal/badgeType/currencyType to get the amount
app.get('/recent/:cType1/:cType2/:limit', function(req, res) {
    console.log(req.params);
    getRecents(req.params.cType1, req.params.cType2, parseInt(req.params.limit), (r) => {
        return res.send(r.toString());
    })
});
app.use('/static', express.static('static'));
app.use('/react', express.static('build'));

port = process.env.PORT || config.webport;
console.log("Listening on port " + port);
app.listen(port);
