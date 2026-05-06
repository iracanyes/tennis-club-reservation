
class APIService {
  private static instance: APIService;
  private readonly baseUrl: string = import.meta.env.VITE_API_URL;
  private constructor() {}

  public static getInstance() {
    if (!APIService.instance) {
      APIService.instance = new APIService();
    }
    return APIService.instance;
  }

  public async post(urlPath: string, payload: any): Promise<any> {
    try{
      const response = await fetch(
        this.baseUrl + urlPath,
        {
          method: 'POST',
          mode: 'cors',
          cache: 'no-cache',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          },
          body: JSON.stringify(payload),
        }
      );

      if(!response.ok){
        throw new Error(`${response.status} : ${response.statusText}`);
      }

      return await response.json();
    }catch (e) {
      console.error(e);
    }
  }

  public async get(urlPath: string): Promise<any> {
    try {
      const response = await fetch(urlPath, {
        method: 'GET',
        mode: 'cors',
        cache: 'default',
        credentials: 'same-origin',
      })

      if(!response.ok){
        throw new Error(`${response.status} : ${response.statusText}`);
      }


      return await response.json();
    }catch (e) {
      console.error(e);
    }

    throw new Error(`Unable to post to ${urlPath}`);
  }

  public async put(urlPath: string, payload: any): Promise<any> {
    try{
      const response = await fetch(urlPath, {
        method: 'PUT',
        mode: 'cors',
        cache: 'default',
        credentials: 'same-origin',
        body: payload,
      })

      if(!response.ok){
        throw new Error(`${response.status} : ${response.statusText}`);
      }

      return await response.json();
    }catch (e) {
      console.error(e);
    }
  }
}

export default APIService;