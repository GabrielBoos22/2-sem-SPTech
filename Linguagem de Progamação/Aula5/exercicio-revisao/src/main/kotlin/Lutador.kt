class Lutador(
    var nome: String,
    var forcaAtaque: Double = 0.0,
    var forcaDefesa: Double = 0.0,
    var vidaAtual: Double = 100.0
) {
    var golpesSofridos = mutableListOf<Double>()

    fun concentrar():Double {
        vidaAtual *= 1.05
        return vidaAtual
    }

    fun treinarLeve(semanas: Int){
        forcaAtaque += semanas
    }
    fun treinarForte(semanas: Int){
        forcaAtaque += semanas * 3
    }
    fun apanhar(quemBate: Lutador){
        if(quemBate.forcaAtaque >= quemBate.forcaDefesa){
            vidaAtual = vidaAtual - quemBate.forcaAtaque - forcaDefesa
            if(vidaAtual < 0){
                vidaAtual = 0.0
            }
            golpesSofridos.add(quemBate.forcaAtaque)
        }

    }
    fun descrever(): String{
        return "Lutador $nome tem $vidaAtual e ja recebeu ${golpesSofridos.size} golpes"
    }

}