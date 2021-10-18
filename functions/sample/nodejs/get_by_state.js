/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
    const db = cloudant.use("dealerships")

    try {
        let dlrList = await db.list({ include_docs: true });
        dlrList.rows = dlrList.rows.filter((row) => { return row.doc.st == params.STATE });
        let output = dlrList.rows.map((row) => {
            return {
                id: row.doc.id,
                city: row.doc.city,
                state: row.doc.state,
                st: row.doc.st,
                address: row.doc.address,
                zip: row.doc.zip,
                lat: row.doc.lat,
                long: row.doc.long
            }
        })
        return { "dealers": output };
    } catch (error) {
        return { error: error.description };
    }

}