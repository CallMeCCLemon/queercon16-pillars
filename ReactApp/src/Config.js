/******************************************************************************
 *    Author: Michael Frohlich
 *      Date: 2019
 * Copyright: 2019 Michael Frohlich - Modified BSD License
 *****************************************************************************/

export default {
    // NO TRAILING SLASH
    apiEndpoint: "http://localhost:8090",

    // number of milliseconds between requests
    apiInterval: 1000,

    // selects which pair of currencies to display
    // 0 == LOCKS, KEYS
    // 1 == COINS, COCKTAILS
    // 2 == CAMERA, FLAG
    currencyType: 0,

    icons: {
        0: "/static/lock.png",
        1: "/static/coin.png",
        2: "/static/camera.png",
        3: "/static/key.png",
        4: "/static/cocktail.png",
        5: "/static/flag.png"
    },

    recent_limit: 6,

    goal: 25000
}