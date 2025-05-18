export const Globalization={
    dateFormat: 'DD/MM/YYYY',
    dateFormat2: (_dt:string, includeHours:boolean)=>{
        try{
            if(_dt === null){
                throw Error('');
            }
            
            const dt = new Date(_dt);
            if (includeHours){
                return dt.toLocaleDateString('es-AR', { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12:true });
            }else{
                return dt.toLocaleDateString('es-AR', { year: "numeric", month: "2-digit", day: "2-digit"});
            }
        }catch(e){
            return '';
        }
    },
    getCurrentDateTime: ()=> {
        const now = new Date();
    
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
    
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
    
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    currencyFormat: new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
    }),
    percentFormat: new Intl.NumberFormat('es-AR', {
        style: 'percent',
        minimumFractionDigits: 2
    })
}