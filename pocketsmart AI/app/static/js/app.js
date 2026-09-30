const TOKEN_KEY = "pocketsmart_token";


function getToken() {

    return localStorage.getItem(
        TOKEN_KEY
    );
}


function requireLogin() {

    if (!getToken()) {

        window.location.href = "/login";

        return false;
    }

    return true;
}


function authHeaders() {

    const token = getToken();

    if (!token) {

        return {};
    }

    return {
        Authorization:
            "Bearer " + token
    };
}


async function api(
    url,
    options = {}
) {

    options.headers = {
        ...(options.headers || {}),
        ...authHeaders(),
    };


    const response = await fetch(
        url,
        options
    );


    const data =
        await response
            .json()
            .catch(
                () => ({
                    detail:
                        "Invalid server response",
                })
            );


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );
    }


    return data;
}


// =========================================================
// RESULT RENDERING
// =========================================================

function renderResults(data) {

    const element =
        document.querySelector(
            "#results"
        );


    if (!element) {

        return;
    }


    const recommendations =
        data.recommendations || [];


    const tips =
        data.tips || [];


    element.innerHTML = `

        <div class="result">

            <div class="card">

                <p class="eyebrow">
                    ${escapeHtml(
                        String(
                            data.source ||
                            "recommendation"
                        ).toUpperCase()
                    )}
                </p>

                <h2>
                    ${escapeHtml(
                        data.summary || ""
                    )}
                </h2>

                <p>

                    Budget:
                    ₹${Number(
                        data.budget || 0
                    ).toLocaleString("en-IN")}

                    ·

                    Allocated:
                    ₹${Number(
                        data.allocated_total || 0
                    ).toLocaleString("en-IN")}

                </p>

            </div>


            <div
                class="grid"
                style="margin-top:18px"
            >

                ${recommendations.map(
                    item => `

                    <div class="card rec">

                        <div>

                            <span class="tag">

                                ${escapeHtml(
                                    item.platform || ""
                                )}

                            </span>

                            <h3>
                                ${escapeHtml(
                                    item.name || ""
                                )}
                            </h3>

                            <p>
                                ${escapeHtml(
                                    item.description || ""
                                )}
                            </p>

                            <a
                                href="${escapeAttribute(
                                    item.url || "#"
                                )}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >

                                Search on
                                ${escapeHtml(
                                    item.platform || "platform"
                                )}

                                ↗

                            </a>

                        </div>


                        <div class="price">

                            ₹${Number(
                                item.price || 0
                            ).toLocaleString("en-IN")}

                        </div>

                    </div>

                `
                ).join("")}

            </div>


            <div
                class="card"
                style="margin-top:18px"
            >

                <b>
                    Planning Tips
                </b>

                <ul>

                    ${tips.map(
                        tip =>
                            `<li>${escapeHtml(
                                tip
                            )}</li>`
                    ).join("")}

                </ul>

            </div>

        </div>
    `;
}


// =========================================================
// SECURITY HELPERS
// =========================================================

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function escapeAttribute(value) {

    return escapeHtml(value);
}


// =========================================================
// HOME FORM
// =========================================================

const homeForm =
    document.querySelector(
        "#homeForm"
    );


if (homeForm) {

    homeForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            if (!requireLogin()) {

                return;
            }


            const formData =
                new FormData(
                    homeForm
                );


            const data =
                Object.fromEntries(
                    formData.entries()
                );


            data.budget =
                Number(
                    data.budget
                );


            data.rooms =
                data.rooms
                    ? data.rooms
                        .split(",")
                        .map(
                            value =>
                                value.trim()
                        )
                        .filter(Boolean)
                    : [];


            data.items =
                data.items
                    ? data.items
                        .split(",")
                        .map(
                            value =>
                                value.trim()
                        )
                        .filter(Boolean)
                    : [];


            const resultElement =
                document.querySelector(
                    "#results"
                );


            resultElement.innerHTML =
                `<p class="loading">
                    Generating your home plan...
                </p>`;


            try {

                const result =
                    await api(
                        "/api/generate-home",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",
                            },

                            body:
                                JSON.stringify(
                                    data
                                ),
                        }
                    );


                renderResults(
                    result
                );

            } catch (error) {

                resultElement.innerHTML =
                    `<div class="card">
                        Error:
                        ${escapeHtml(
                            error.message
                        )}
                    </div>`;
            }
        }
    );
}


// =========================================================
// PARTY FORM
// =========================================================

const partyForm =
    document.querySelector(
        "#partyForm"
    );


if (partyForm) {

    partyForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            if (!requireLogin()) {

                return;
            }


            const formData =
                new FormData(
                    partyForm
                );


            const data =
                Object.fromEntries(
                    formData.entries()
                );


            data.budget =
                Number(
                    data.budget
                );


            data.guests =
                Number(
                    data.guests
                );


            const resultElement =
                document.querySelector(
                    "#results"
                );


            resultElement.innerHTML =
                `<p class="loading">
                    Generating your party plan...
                </p>`;


            try {

                const result =
                    await api(
                        "/api/generate-party",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",
                            },

                            body:
                                JSON.stringify(
                                    data
                                ),
                        }
                    );


                renderResults(
                    result
                );

            } catch (error) {

                resultElement.innerHTML =
                    `<div class="card">
                        Error:
                        ${escapeHtml(
                            error.message
                        )}
                    </div>`;
            }
        }
    );
}


// =========================================================
// JEWELRY FORM
// =========================================================

const jewelryForm =
    document.querySelector(
        "#jewelryForm"
    );


if (jewelryForm) {

    jewelryForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            if (!requireLogin()) {

                return;
            }


            const resultElement =
                document.querySelector(
                    "#results"
                );


            resultElement.innerHTML =
                `<p class="loading">
                    Analyzing your jewelry preferences...
                </p>`;


            try {

                const formData =
                    new FormData(
                        jewelryForm
                    );


                const result =
                    await api(
                        "/api/generate-jewelry",
                        {
                            method: "POST",
                            body: formData,
                        }
                    );


                renderResults(
                    result
                );

            } catch (error) {

                resultElement.innerHTML =
                    `<div class="card">
                        Error:
                        ${escapeHtml(
                            error.message
                        )}
                    </div>`;
            }
        }
    );
}


// =========================================================
// LOGIN
// =========================================================

const loginForm =
    document.querySelector(
        "#loginForm"
    );


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const message =
                document.querySelector(
                    "#msg"
                );


            try {

                const formData =
                    new FormData(
                        loginForm
                    );


                const data =
                    Object.fromEntries(
                        formData.entries()
                    );


                const result =
                    await api(
                        "/api/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",
                            },

                            body:
                                JSON.stringify(
                                    data
                                ),
                        }
                    );


                localStorage.setItem(
                    TOKEN_KEY,
                    result.access_token
                );


                window.location.href =
                    "/dashboard";

            } catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}


// =========================================================
// REGISTER
// =========================================================

const registerForm =
    document.querySelector(
        "#registerForm"
    );


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const message =
                document.querySelector(
                    "#msg"
                );


            try {

                const formData =
                    new FormData(
                        registerForm
                    );


                const data =
                    Object.fromEntries(
                        formData.entries()
                    );


                const result =
                    await api(
                        "/api/register",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",
                            },

                            body:
                                JSON.stringify(
                                    data
                                ),
                        }
                    );


                localStorage.setItem(
                    TOKEN_KEY,
                    result.access_token
                );


                window.location.href =
                    "/dashboard";

            } catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}


// =========================================================
// DASHBOARD
// =========================================================

async function loadDashboard() {

    const profile =
        document.querySelector(
            "#profile"
        );


    const historyElement =
        document.querySelector(
            "#history"
        );


    if (
        !profile ||
        !historyElement
    ) {

        return;
    }


    if (!requireLogin()) {

        return;
    }


    try {

        const session =
            await api(
                "/api/session-info"
            );


        profile.innerHTML = `

            <b>
                ${escapeHtml(
                    session.name || ""
                )}
            </b>

            <p>
                ${escapeHtml(
                    session.email || ""
                )}
            </p>

        `;


        const history =
            await api(
                "/api/history"
            );


        if (!history.length) {

            historyElement.innerHTML =
                `<div class="card">
                    No recommendations yet.
                </div>`;

            return;
        }


        historyElement.innerHTML =
            history.map(
                item => `

                <div class="card">

                    <span class="tag">
                        ${escapeHtml(
                            item.planner
                        )}
                    </span>

                    <h3>
                        Recommendation
                        #${item.id}
                    </h3>

                    <p>
                        ${new Date(
                            item.created_at
                        ).toLocaleString()}
                    </p>

                    <button
                        class="btn ghost"
                        onclick="viewHistory(
                            ${item.id}
                        )"
                    >
                        View
                    </button>

                </div>
            `
            ).join("");

    } catch (error) {

        localStorage.removeItem(
            TOKEN_KEY
        );

        window.location.href =
            "/login";
    }
}


// =========================================================
// HISTORY DETAIL
// =========================================================

async function viewHistory(
    historyId
) {

    try {

        const result =
            await api(
                `/api/recommendations-details/${historyId}`
            );


        const results =
            document.querySelector(
                "#results"
            );


        if (!results) {

            window.location.href =
                "/planner/home";

            return;
        }


        renderResults(
            result
        );


        window.scrollTo(
            0,
            document.body.scrollHeight
        );

    } catch (error) {

        alert(
            error.message
        );
    }
}


// =========================================================
// LOGOUT
// =========================================================

function logout() {

    localStorage.removeItem(
        TOKEN_KEY
    );

    window.location.href =
        "/login";
}


loadDashboard();