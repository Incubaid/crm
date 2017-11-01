import axios from 'axios'

export const queryAllDeals = `
query allDeals {
    deals {
      edges{
        node{
          uid,
          name,
          amount,
          dealState,
          contact {
              firstname
              lastname
          }
        }
      }
    }
  }
`

export function getAllDeals() {
    return axios.post(`http://27c9db6b.ngrok.io/api`, {'query': queryAllDeals }, {'headers':{'Content-Type':'application/json'}})
}