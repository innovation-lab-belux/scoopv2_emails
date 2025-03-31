const schedule = require('node-schedule');
const axios = require('axios');
const nodemailer = require('nodemailer');
const { v4: uuidv4 } = require('uuid');

// ---------- Weekly Task ----------
async function weeklyTask() {
    const customers = ["carrefour", "colruyt"];
    const chatId = await createChat();

    for (const customer of customers) {
        await askAgentInChat("b4a59ce2-1afc-4793-bd55-ebd2e5bab313", chatId, customer);
    }

    // Send an email after the task is completed
    const subject = "test subject";
    const body = "testing body.";
    const recipientEmail = "liano.caekebeke@sap.com";
    sendEmail(subject, body, recipientEmail);
}

// Schedule the task to run every Thursday at 14:00
schedule.scheduleJob('0 14 * * 4', weeklyTask);

// ---------- Agent API ----------
async function getToken() {
    const url = "https://agents-y0yj1uar.authentication.eu12.hana.ondemand.com/oauth/token";
    const headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    };

    const data = new URLSearchParams({
        "grant_type": "client_credentials",
        "client_id": "sb-dffecf4b-ac7b-486a-bf64-a5891a63985f!b726223|unified-ai-agent!b268611",
        "client_secret": "064dda8b-5fcc-4bee-a785-57e37d2e502a$zqrV5_n7095m4ZEdtISL1WuKIJErm4NtcR9DtVKae2A="
    });

    try {
        const response = await axios.post(url, data, { headers });
        if (response.status === 200) {
            return response.data.access_token;
        } else {
            console.error(`Error: ${response.status} - ${response.data}`);
        }
    } catch (error) {
        console.error(`Error fetching token: ${error.message}`);
    }
}

async function createChat(agent = "b4a59ce2-1afc-4793-bd55-ebd2e5bab313", name = "New conversation") {
    const newChatId = uuidv4();

    const newChatData = {
        ID: newChatId,
        name: name,
        history: [
            {
                ID: "01234567-89ab-cdef-0123-456789abcdef",
                trace: [
                    {
                        ID: "01234567-89ab-cdef-0123-456789abcdef",
                        index: 0,
                        fromId: "string",
                        toId: "string",
                        type: "start",
                        tokenConsumption: [
                            {
                                ID: "01234567-89ab-cdef-0123-456789abcdef",
                                modelName: "OpenAiGpt4o",
                                inputTokens: 0,
                                outputTokens: 0
                            }
                        ],
                        data: "string"
                    }
                ],
                type: "questionForAgent",
                sender: "ai",
                content: "string",
                outputFormat: "string",
                outputFormatOptions: "string",
                rating: 0,
                inputValues: [
                    {
                        ID: "01234567-89ab-cdef-0123-456789abcdef",
                        name: "string",
                        description: "string",
                        type: "string",
                        possibleValues: ["string"],
                        suggestions: ["string"]
                    }
                ],
                source: "string",
                canceled: false
            }
        ]
    };

    const urlRequest = `/${agent}/chats`;
    await postAgentsAPI(urlRequest, newChatData);
    return newChatId;
}

async function postAgentsAPI(urlRequest, data = null) {
    const token = await getToken();

    const headers = {
        "accept": "application/json",
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };

    const url = `https://unified-ai-agent-srv-unified-agent.c-1228ddd.stage.kyma.ondemand.com/api/v1/Agents${urlRequest}`;

    try {
        const response = await axios.post(url, data, { headers });
        if (response.status === 200) {
            return response.data;
        } else {
            console.error(`Error: ${response.status} - ${response.data}`);
            return response.status;
        }
    } catch (error) {
        console.error(`Error in PostAgentsAPI: ${error.message}`);
    }
}

async function askAgentInChat(agent, chat, msg) {
    const newMessageData = {
        msg: msg,
        async: false,
        destination: "AGENT_CALLBACK",
        outputFormat: "Markdown"
    };

    const urlRequest = `/${agent}/chats(${chat})/UnifiedAiAgentService.sendMessage`;
    const answer = await postAgentsAPI(urlRequest, newMessageData);
    return answer;
}

// ---------- Email Sending ----------
function sendEmail(subject, body, recipientEmail) {
    const senderEmail = "sap.scoop.news@gmail.com";
    const senderPassword = "omhs msje tsyy rzuf";

    const transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
            user: senderEmail,
            pass: senderPassword
        }
    });

    const mailOptions = {
        from: senderEmail,
        to: recipientEmail,
        subject: subject,
        text: body
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error(`Failed to send email: ${error.message}`);
        } else {
            console.log(`Email sent successfully: ${info.response}`);
        }
    });
}