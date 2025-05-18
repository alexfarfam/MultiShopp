
const qualifications = ref<string[]>(['Sin calificar', 'Terrible', 'Malo', 'Normal', 'Bueno', 'Óptimo']);
const daysOfWeek = [
    { value: 'MON', label: 'Lunes' },
    { value: 'TUE', label: 'Martes' },
    { value: 'WED', label: 'Miércoles' },
    { value: 'THU', label: 'Jueves' },
    { value: 'FRI', label: 'Viernes' },
    { value: 'SAT', label: 'Sábado' },
    { value: 'SUN', label: 'Domingo' },
];
const daysOfWeek2:any={
    'MON': 'Lunes' ,
    'TUE':'Martes',
    'WED':'Miércoles',
    'THU':'Jueves',
    'FRI':'Viernes',
    'SAT':'Sábado',
    'SUN':'Domingo'
};

export{
    qualifications,
    daysOfWeek,
    daysOfWeek2
}