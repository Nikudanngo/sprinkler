'use strict';
const express = require('express');
const app = express()

// get通信処理
app.get('/', (req, res) => res.send('これは散水システムの操作ページです。'));

app.get('/On', (req, res) => {
    res.send('散水を開始します。');
    const exec = require('child_process').exec;
    var yourscript = exec('sh On.sh',
    (error, stdout, stderr) => {
        console.log(stdout);
        console.log(stderr);
        if (error !== null) {
            console.log('exec error: ${error}');
        }
    });
});

app.get('/Off', (req, res) => {
    res.send('散水を終了します。');
    const exec = require('child_process').exec;
    var yourscript = exec('sh Off.sh',
    (error, stdout, stderr) => {
        console.log(stdout);
        console.log(stderr);
        if (error !== null) {
            console.log('exec error: ${error}');
        }
    });
});

app.listen(3000, () => console.log('Example app listening on port 3000!'));

// 定期実行処理
const cron = require('node-cron');
cron.schedule('0 0 7,18 * * *', () => {     // 毎日7:00と18:00に"ok"と出力，水やり
    console.log('ok')
    // shを実行する処理 意味わからん
    const exec = require('child_process').exec;
    var yourscript = exec('sh ServoOn.sh',
        (error, stdout, stderr) => {
            console.log(stdout);
            console.log(stderr);
            if (error !== null) {
                console.log('exec error: ${error}');
            }
        });
});     