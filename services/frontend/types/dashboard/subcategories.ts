
interface SubCategoryItem{
    id: number,
    title: string,
    category__id: string,
    category__title: string,
    description: string,
    image: string
};
interface SubCategoryForm{
    title: string,
    category: string,
    description: string,
    image: string
};

export type{
    SubCategoryItem,
    SubCategoryForm,
}