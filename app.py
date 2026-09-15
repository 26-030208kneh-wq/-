import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="체스 게임",
    page_icon="♟️",
    layout="centered"
)

components.html(
r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #f3f5f4;
    font-family: Arial, sans-serif;
}

#app {
    max-width: 650px;
    margin: auto;
    text-align: center;
}

.title {
    font-size: 42px;
    font-weight: bold;
    color: #173d2b;
    margin-top: 15px;
}

.subtitle {
    color: #68756e;
    margin-bottom: 25px;
}

/* 메인 */

.start-box {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 5px 20px rgba(0,0,0,.1);
}

.big-chess {
    font-size: 70px;
    margin-bottom: 10px;
}

.start-title {
    font-size: 27px;
    font-weight: bold;
    color: #173d2b;
}

.start-text {
    color: #777;
    margin: 10px 0 25px;
}

.start-button {
    width: 100%;
    border: none;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

.ai-button {
    background: #1976d2;
}

.friend-button {
    background: #168447;
}

/* 게임 */

#game {
    display: none;
}

.info {
    background: white;
    border-radius: 15px;
    padding: 15px;
    margin: 15px 0;
    box-shadow: 0 3px 12px rgba(0,0,0,.08);
}

.turn {
    font-size: 18px;
    font-weight: bold;
    color: #333;
}

/* 체스판 */

.board-wrap {
    display: flex;
    justify-content: center;
}

.board {
    width: min(94vw, 600px);
    height: min(94vw, 600px);

    display: grid;
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat(8, 1fr);

    border: 7px solid #222;
    box-shadow: 0 8px 20px rgba(0,0,0,.3);
}

/* 칸 */

.square {
    position: relative;

    display: flex;
    align-items: center;
    justify-content: center;

    cursor: pointer;
}

.light {
    background: #f0d9b5;
}

.dark {
    background: #b58863;
}

.selected {
    box-shadow: inset 0 0 0 5px #ffe600;
}

.possible {
    background: #8bc34a;
}

.capture {
    box-shadow: inset 0 0 0 5px #e53935;
}

/* 말 */

.piece {
    font-size: clamp(30px, 8vw, 65px);
    line-height: 1;

    user-select: none;

    filter:
        drop-shadow(2px 3px 2px rgba(0,0,0,.35));
}

/* 아래 버튼 */

.buttons {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.game-button {
    flex: 1;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

.restart {
    background: #168447;
    color: white;
}

.home {
    background: #555;
    color: white;
}

/* 결과 */

.result {
    display: none;

    background: white;
    margin-top: 20px;
    padding: 25px;

    border-radius: 15px;

    font-size: 24px;
    font-weight: bold;

    box-shadow: 0 4px 15px rgba(0,0,0,.12);
}

.result button {
    margin-top: 15px;

    border: none;
    border-radius: 10px;

    padding: 14px 30px;

    background: #168447;
    color: white;

    font-size: 18px;
    font-weight: bold;

    cursor: pointer;
}
</style>
</head>


<body>

<div id="app">

    <!-- ==========================
         메인 화면
         ========================== -->

    <div id="home">

        <div class="title">
            ♟️ 체스 ♟️
        </div>

        <div class="subtitle">
            나만의 체스 게임
        </div>

        <div class="start-box">

            <div class="big-chess">
                ♔ ♚
            </div>

            <div class="start-title">
                게임을 시작하세요
            </div>

            <div class="start-text">
                게임 방식을 선택해주세요.
            </div>

            <button
                class="start-button ai-button"
                onclick="startGame('ai')"
            >
                🤖 AI와 하기
            </button>

            <button
                class="start-button friend-button"
                onclick="startGame('friend')"
            >
                👥 친구와 하기
            </button>

        </div>

    </div>


    <!-- ==========================
         게임 화면
         ========================== -->

    <div id="game">

        <div class="title">
            ♟️ 체스
        </div>

        <div class="info">

            <div
                class="turn"
                id="turnText"
            >
                ⚪ 백의 차례
            </div>

        </div>


        <div class="board-wrap">

            <div
                class="board"
                id="board"
            ></div>

        </div>


        <div
            class="result"
            id="result"
        ></div>


        <div class="buttons">

            <button
                class="game-button restart"
                onclick="restartGame()"
            >
                🔄 다시 시작
            </button>

            <button
                class="game-button home"
                onclick="goHome()"
            >
                🏠 처음으로
            </button>

        </div>

    </div>

</div>


<script>

/* ======================================
   체스 설정
   ====================================== */

const EMPTY = "";

let board = [];

let currentPlayer = "white";

let selected = null;

let gameMode = "ai";

let gameOver = false;


/* 체스 말 */

const whitePieces = {
    king: "♔",
    queen: "♕",
    rook: "♖",
    bishop: "♗",
    knight: "♘",
    pawn: "♙"
};

const blackPieces = {
    king: "♚",
    queen: "♛",
    rook: "♜",
    bishop: "♝",
    knight: "♞",
    pawn: "♟"
};


/* ======================================
   보드 만들기
   ====================================== */

function createBoard() {

    board = Array.from(
        {length: 8},
        () => Array(8).fill(null)
    );


    /* 흑 */

    board[0][0] = {type:"rook", color:"black"};
    board[0][1] = {type:"knight", color:"black"};
    board[0][2] = {type:"bishop", color:"black"};
    board[0][3] = {type:"queen", color:"black"};
    board[0][4] = {type:"king", color:"black"};
    board[0][5] = {type:"bishop", color:"black"};
    board[0][6] = {type:"knight", color:"black"};
    board[0][7] = {type:"rook", color:"black"};

    for (let c = 0; c < 8; c++) {
        board[1][c] = {
            type:"pawn",
            color:"black"
        };
    }


    /* 백 */

    board[7][0] = {type:"rook", color:"white"};
    board[7][1] = {type:"knight", color:"white"};
    board[7][2] = {type:"bishop", color:"white"};
    board[7][3] = {type:"queen", color:"white"};
    board[7][4] = {type:"king", color:"white"};
    board[7][5] = {type:"bishop", color:"white"};
    board[7][6] = {type:"knight", color:"white"};
    board[7][7] = {type:"rook", color:"white"};

    for (let c = 0; c < 8; c++) {
        board[6][c] = {
            type:"pawn",
            color:"white"
        };
    }

}


/* ======================================
   보드 안인지
   ====================================== */

function inside(r,c) {

    return (
        r >= 0 &&
        r < 8 &&
        c >= 0 &&
        c < 8
    );

}


/* ======================================
   같은 색인지
   ====================================== */

function sameColor(piece,color) {

    return piece && piece.color === color;

}


/* ======================================
   말 이동 가능 위치
   ====================================== */

function getMoves(r,c) {

    const piece = board[r][c];

    if (!piece) {
        return [];
    }

    let moves = [];

    const color = piece.color;

    const enemy =
        color === "white"
        ? "black"
        : "white";


    /* =========================
       폰
       ========================= */

    if (piece.type === "pawn") {

        const direction =
            color === "white"
            ? -1
            : 1;

        const startRow =
            color === "white"
            ? 6
            : 1;


        let nr = r + direction;


        if (
            inside(nr,c) &&
            !board[nr][c]
        ) {

            moves.push([nr,c]);


            if (
                r === startRow &&
                !board[
                    r + direction * 2
                ][c]
            ) {

                moves.push([
                    r + direction * 2,
                    c
                ]);

            }

        }


        for (
            const dc of [-1,1]
        ) {

            const nc = c + dc;

            if (
                inside(nr,nc) &&
                board[nr][nc] &&
                board[nr][nc].color === enemy
            ) {

                moves.push([
                    nr,
                    nc
                ]);

            }

        }

    }


    /* =========================
       나이트
       ========================= */

    if (piece.type === "knight") {

        const jumps = [

            [-2,-1],
            [-2,1],
            [-1,-2],
            [-1,2],
            [1,-2],
            [1,2],
            [2,-1],
            [2,1]

        ];


        for (
            const jump of jumps
        ) {

            const nr = r + jump[0];
            const nc = c + jump[1];


            if (!inside(nr,nc)) {
                continue;
            }


            if (
                !board[nr][nc] ||
                board[nr][nc].color !== color
            ) {

                moves.push([
                    nr,
                    nc
                ]);

            }

        }

    }


    /* =========================
       킹
       ========================= */

    if (piece.type === "king") {

        for (let dr=-1; dr<=1; dr++) {

            for (let dc=-1; dc<=1; dc++) {

                if (dr === 0 && dc === 0) {
                    continue;
                }

                const nr = r + dr;
                const nc = c + dc;


                if (!inside(nr,nc)) {
                    continue;
                }


                if (
                    !board[nr][nc] ||
                    board[nr][nc].color !== color
                ) {

                    moves.push([
                        nr,
                        nc
                    ]);

                }

            }

        }

    }


    /* =========================
       룩 / 비숍 / 퀸
       ========================= */

    if (
        piece.type === "rook" ||
        piece.type === "bishop" ||
        piece.type === "queen"
    ) {

        let dirs = [];


        if (
            piece.type === "rook" ||
            piece.type === "queen"
        ) {

            dirs.push(
                [-1,0],
                [1,0],
                [0,-1],
                [0,1]
            );

        }


        if (
            piece.type === "bishop" ||
            piece.type === "queen"
        ) {

            dirs.push(
                [-1,-1],
                [-1,1],
                [1,-1],
                [1,1]
            );

        }


        for (
            const dir of dirs
        ) {

            let nr = r + dir[0];
            let nc = c + dir[1];


            while (
                inside(nr,nc)
            ) {

                if (!board[nr][nc]) {

                    moves.push([
                        nr,
                        nc
                    ]);

                }

                else {

                    if (
                        board[nr][nc].color !== color
                    ) {

                        moves.push([
                            nr,
                            nc
                        ]);

                    }

                    break;

                }


                nr += dir[0];
                nc += dir[1];

            }

        }

    }


    return moves;

}


/* ======================================
   보드 그리기
   ====================================== */

function renderBoard() {

    const boardElement =
        document.getElementById("board");

    boardElement.innerHTML = "";


    let possibleMoves = [];

    if (selected) {

        possibleMoves =
            getMoves(
                selected[0],
                selected[1]
            );

    }


    for (let r=0; r<8; r++) {

        for (let c=0; c<8; c++) {

            const square =
                document.createElement("div");

            square.className =
                "square " +
                (
                    (r+c)%2 === 0
                    ? "light"
                    : "dark"
                );


            /* 선택 */

            if (
                selected &&
                selected[0] === r &&
                selected[1] === c
            ) {

                square.classList.add(
                    "selected"
                );

            }


            /* 가능한 이동 */

            const possible =
                possibleMoves.some(
                    move =>
                        move[0] === r &&
                        move[1] === c
                );


            if (possible) {

                if (board[r][c]) {

                    square.classList.add(
                        "capture"
                    );

                }

                else {

                    square.classList.add(
                        "possible"
                    );

                }

            }


            /* 말 */

            if (board[r][c]) {

                const piece =
                    document.createElement("div");

                piece.className = "piece";


                if (
                    board[r][c].color === "white"
                ) {

                    piece.textContent =
                        whitePieces[
                            board[r][c].type
                        ];

                }

                else {

                    piece.textContent =
                        blackPieces[
                            board[r][c].type
                        ];

                }


                square.appendChild(
                    piece
                );

            }


            square.onclick = function() {

                clickSquare(r,c);

            };


            boardElement.appendChild(
                square
            );

        }

    }

}


/* ======================================
   칸 클릭
   ====================================== */

function clickSquare(r,c) {

    if (gameOver) {
        return;
    }


    /* AI 차례 */

    if (
        gameMode === "ai" &&
        currentPlayer === "black"
    ) {

        return;

    }


    const piece =
        board[r][c];


    /* 아무것도 선택 안 함 */

    if (!selected) {

        if (
            piece &&
            piece.color === currentPlayer
        ) {

            selected = [r,c];

            renderBoard();

        }

        return;

    }


    /* 다른 내 말을 클릭 */

    if (
        piece &&
        piece.color === currentPlayer
    ) {

        selected = [r,c];

        renderBoard();

        return;

    }


    /* 이동 */

    const moves =
        getMoves(
            selected[0],
            selected[1]
        );


    const valid =
        moves.some(
            move =>
                move[0] === r &&
                move[1] === c
        );


    if (!valid) {

        selected = null;

        renderBoard();

        return;

    }


    movePiece(
        selected[0],
        selected[1],
        r,
        c
    );


    selected = null;

    currentPlayer =
        currentPlayer === "white"
        ? "black"
        : "white";


    renderBoard();

    checkGame();


    /* AI */

    if (
        gameMode === "ai" &&
        currentPlayer === "black" &&
        !gameOver
    ) {

        setTimeout(
            aiMove,
            600
        );

    }

}


/* ======================================
   말 이동
   ====================================== */

function movePiece(
    r1,c1,r2,c2
) {

    const piece =
        board[r1][c1];


    board[r2][c2] =
        piece;


    board[r1][c1] =
        null;


    /* 폰 프로모션 */

    if (
        piece.type === "pawn" &&
        (
            r2 === 0 ||
            r2 === 7
        )
    ) {

        piece.type = "queen";

    }

}


/* ======================================
   AI
   ====================================== */

function aiMove() {

    if (gameOver) {
        return;
    }


    let choices = [];


    for (let r=0; r<8; r++) {

        for (let c=0; c<8; c++) {

            const piece =
                board[r][c];


            if (
                piece &&
                piece.color === "black"
            ) {

                const moves =
                    getMoves(r,c);


                for (
                    const move of moves
                ) {

                    choices.push({
                        from:[r,c],
                        to:move,
                        capture:
                            board[
                                move[0]
                            ][
                                move[1]
                            ] !== null
                    });

                }

            }

        }

    }


    if (choices.length === 0) {

        finishGame(
            "🎉 당신의 승리!"
        );

        return;

    }


    /* 잡을 수 있는 말을 우선 */

    const captures =
        choices.filter(
            move => move.capture
        );


    let choice;


    if (captures.length > 0) {

        choice =
            captures[
                Math.floor(
                    Math.random() *
                    captures.length
                )
            ];

    }

    else {

        choice =
            choices[
                Math.floor(
                    Math.random() *
                    choices.length
                )
            ];

    }


    movePiece(
        choice.from[0],
        choice.from[1],
        choice.to[0],
        choice.to[1]
    );


    currentPlayer = "white";


    renderBoard();

    checkGame();

}


/* ======================================
   게임 확인
   ====================================== */

function checkGame() {

    let whiteKing = false;
    let blackKing = false;


    for (let r=0; r<8; r++) {

        for (let c=0; c<8; c++) {

            if (
                board[r][c] &&
                board[r][c].type === "king"
            ) {

                if (
                    board[r][c].color === "white"
                ) {

                    whiteKing = true;

                }

                else {

                    blackKing = true;

                }

            }

        }

    }


    if (!whiteKing) {

        finishGame(
            "♚ 흑의 승리!"
        );

        return;

    }


    if (!blackKing) {

        finishGame(
            "♔ 백의 승리!"
        );

        return;

    }


    updateTurn();

}


/* ======================================
   차례 표시
   ====================================== */

function updateTurn() {

    const text =
        document.getElementById(
            "turnText"
        );


    if (gameMode === "ai") {

        if (
            currentPlayer === "white"
        ) {

            text.textContent =
                "⚪ 당신의 차례";

        }

        else {

            text.textContent =
                "⚫ AI가 생각 중...";

        }

    }

    else {

        if (
            currentPlayer === "white"
        ) {

            text.textContent =
                "⚪ 백의 차례";

        }

        else {

            text.textContent =
                "⚫ 흑의 차례";

        }

    }

}


/* ======================================
   게임 종료
   ====================================== */

function finishGame(message) {

    gameOver = true;


    const result =
        document.getElementById(
            "result"
        );


    result.style.display =
        "block";


    result.innerHTML =
        message +
        "<br><br>" +
        '<button onclick="goHome()">' +
        "🔄 다시하기" +
        "</button>";


    setTimeout(
        function() {

            result.scrollIntoView({
                behavior:"smooth",
                block:"center"
            });

        },
        100
    );

}


/* ======================================
   게임 시작
   ====================================== */

function startGame(mode) {

    gameMode = mode;


    document.getElementById(
        "home"
    ).style.display =
        "none";


    document.getElementById(
        "game"
    ).style.display =
        "block";


    restartGame();

}


/* ======================================
   다시 시작
   ====================================== */

function restartGame() {

    createBoard();


    currentPlayer =
        "white";


    selected = null;


    gameOver = false;


    document.getElementById(
        "result"
    ).style.display =
        "none";


    renderBoard();

    updateTurn();

}


/* ======================================
   메인으로
   ====================================== */

function goHome() {

    document.getElementById(
        "game"
    ).style.display =
        "none";


    document.getElementById(
        "home"
    ).style.display =
        "block";


    document.getElementById(
        "result"
    ).style.display =
        "none";


    createBoard();


    currentPlayer =
        "white";


    selected = null;

    gameOver = false;

}

</script>

</body>
</html>
""",
    height=1100,
    scrolling=True
)
