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
        return { "dealers": dlrList };
    } catch (error) {
        return { error: error.description };
    }

}
