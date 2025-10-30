const APIServer = "http://localhost:5000";

export async function getServers() {
    const response = await fetch(APIServer + "/api/get-servers");
    return await response.json();
}