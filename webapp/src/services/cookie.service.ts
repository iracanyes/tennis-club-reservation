import {isNil} from "lodash";

class CookieService {
  private static instance : CookieService;

  public static getInstance(): CookieService{
    if(isNil(CookieService.instance)){
      CookieService.instance = new CookieService();
    }

    return CookieService.instance;
  }

  public setCookie(name: string, value : string, days : number){
    let expires = "";
    if (days){
      let date = new Date();
      date.setTime(date.getTime() + days*24*60*60*1000);
      expires = "; expires=" + date.toUTCString();

    }

    document.cookie = name + "=" + ( value || "" ) + expires + ";path=/";
  }

  public getCookie(name: string){
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');

    for(const element of ca) {
      let c = element;

      while (c.startsWith(' '))
        c = c.substring(1, c.length);

      if (c.startsWith(nameEQ))
        return c.substring(nameEQ.length, c.length);
    }

    return null;

  }

  public eraseCookie(name: string){
    document.cookie = name + "=; Path=/;";
  }
}

export default CookieService;