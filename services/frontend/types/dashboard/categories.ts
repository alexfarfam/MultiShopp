
interface CategoryItem{
    id: number,
    title: string,
    description: string,
    image: string
};
interface CategoryForm{
    title: string,
    description: string,
    image: string
};

export type{
    CategoryItem,
    CategoryForm,
}