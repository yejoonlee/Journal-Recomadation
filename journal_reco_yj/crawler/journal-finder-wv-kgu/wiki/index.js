const axios = require('axios')
const mysql = require('async-mysql')
const dbconfig   = require('./config/database.js')
const wikiSearchURL = 'https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
const wikiLinkInfoURL = 'https://en.wikipedia.org/w/api.php?action=query&prop=links|extlinks&titles='

let main;

//status: 0: waiting, 1: success, -1: wiki failed
const getWikiSeaarchURL = async keyword => {
    try {
        const url = wikiSearchURL + keyword.replace(/ /g, '+').replace('&','%26')
        const response = await axios.get(url)
        const data = response.data
        return data[3][0] ? data[3][0] : null
    } catch (error) {
        console.log(error)
    }
}

main = async () => {
    let connection, rows
    connection = await mysql.connect(dbconfig)

    rows = await connection.query("SELECT * from a_journal WHERE id not IN (SELECT a_journal_id from a_journal_crawling_log WHERE crawler_type LIKE 'wiki' AND status NOT IN (-1, 1))")

    let countTotal = await connection.query('select count(*) as count from a_journal')
    let countCompleted = await connection.query('select count(*) as count from a_journal_crawling_log WHERE status=1')
    let countWikiFailed = await connection.query('select count(*) as count from a_journal_crawling_log WHERE status=-1')

    console.log('Total: ' + countTotal[0].count + ', Completed: ' + countCompleted[0].count + ', Wiki failed:' + countWikiFailed[0].count)
    let i=1
    for(let row of rows) {
        let updateQuery
        let keyword = row.title
        console.log(i++ + ": " +keyword)

        let hasLog = await connection.query('select count(*) as count from a_journal_crawling_log WHERE a_journal_id=' + row.id)
        if(hasLog[0].count === 0) {
            let res = await connection.query("INSERT INTO a_journal_crawling_log (a_journal_id) VALUES ("+row.id+")")
        }

        let keywordHasJournal = keyword.indexOf('JOURNAL') !== -1
        let firstKeyword = keywordHasJournal ? keyword : keyword + ' (journal)'

        // 첫번째 시도: JOURNAL이 이름에 포함되지 않은 경우 (journal)을 붙여서 질의 - 원래 키워드로 하면 저널이 아닌 다른게 검색되는 경우가 있음
        let result = await getWikiSeaarchURL(firstKeyword)

        if ( result ) { // 첫번째 시도 성공
            console.log('Success: ', result)

            updateQuery = "UPDATE a_journal_crawling_log SET status=1, step1_url='" + result + "' WHERE a_journal_id=" + row.id
        } else { // 첫번째 시도 실패
            console.log('1st failed')
            // 키워드에 저널이 없으면, 원래 키워드로 재시도
            if (! keywordHasJournal) {
                result = await getWikiSeaarchURL(keyword)
                if (result) {
                    console.log('Success on 2nd request: ', result)
                    updateQuery = "UPDATE a_journal_crawling_log SET status=1, step1_url='" + result + "' WHERE a_journal_id=" + row.id
                } else {
                    console.log('2nd failed')
                    updateQuery = "UPDATE a_journal_crawling_log SET status=-1 WHERE a_journal_id=" + row.id
                }
            } else {
                updateQuery = "UPDATE a_journal_crawling_log SET status=-1 WHERE a_journal_id=" + row.id
            }
        }

        let res = await connection.query(await updateQuery)
        // Raw result 저장
        console.log('')
    }
}

    main()

