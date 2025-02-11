
import { URI } from "./conection"
const siteService = {
    async getSites ()  {
        try {
            const response = await fetch(`${URI}/sites`)
            const data = response.json()
            return data
        } catch (error) {
            console.log(error)
        }
    },

    async getSiteById (site_id)  {
        try {
            const response = await fetch(`${URI}/site/${site_id}`)
            const data = response.json()
            return data
        } catch (error) {
            console.log(error)
        }
    },

    async siteDirectory (site_id)  {
        try {
            const response = await fetch(`${URI}/site/${site_id}/all-details`)
            const data = response.json()
            return data
        } catch (error) {
            console.log(error)
        }
    }
}





export {siteService}