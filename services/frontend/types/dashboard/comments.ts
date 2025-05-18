interface CommentForm{
    description: string,
    product: string,
    service: string,
    starts: number
}

interface CommentItem{
   id: number,
   description: string,
   starts: number,
   creation_date: string,
   product__title: string,
   service__title: string,
   responsible__id: number,
   responsible__username: string,

   deleted: boolean
}

export type {
    CommentItem,
    CommentForm
}