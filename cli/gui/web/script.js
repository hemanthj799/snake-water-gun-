let userScore = 0;
let compScore = 0;

function play(user) {
    const choices = ["snake", "water", "gun"];
    const comp = choices[Math.floor(Math.random() * 3)];

    let result = "";

    if (user === comp) result = "Tie!";
    else if (
        (user === "snake" && comp === "water") ||
        (user === "water" && comp === "gun") ||
        (user === "gun" && comp === "snake")
    ) {
        result = "You Win 🎉";
        userScore++;
    } else {
        result = "Computer Wins 🤖";
        compScore++;
    }

    document.getElementById("result").innerText =
        `You: ${user} | Computer: ${comp} → ${result}`;

    document.getElementById("score").innerText =
        `Score → You: ${userScore} | Computer: ${compScore}`;
}