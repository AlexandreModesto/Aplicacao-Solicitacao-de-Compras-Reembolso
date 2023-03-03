# Aplicacao-Solicitacao-de-Compras-Reembolso
Uma aplicação de solicitação, cotação e reembolso para substituir processo manuais

Documentação Aplicação Solicitação

Esta é uma documentação feita a mão, já que eu não implementei o Swagger...
Pois bem, como diria Jack O Estripador vamos por partes
Esta é uma Aplicação que eu acredito não ser REST ou RESTful, já que eu não me guiei pelos padrões propostos por Roy Fielding
e como é a primeira vez que integro uma aplicação com front e backend eu apenas segui o ''fluxo''. Dito isso, essa aplicação foi feita para funcionar localmente já que eu não consegui implementar o APACHE para python visto que eu usei windows.É uma aplicação feita
com Flask (python) e MySQL no backend e HTML,CSS e JAVASCRIPT puro no front.

Ela consiste na conexão das páginas com o banco de dados via requisições do usuário onde algumas rotas enviam emails
automáticos para determinados individuos, essa conexão tambem ocorre localmente com o upload de arquivos salvos em uma pasta local.
O Por que disso? pois essa aplicação tem como objetivo substituir processos de solicitações de compra/reembolso que são feitas
manualmente onde o solicitante planeja uma solicitação, entra para o superior assinar o documento e então seu diretor támbem assina e o
financeiro finaliza. Um processo que envolve imprimir arquivo levar até o assinante 1 depois até o assinante 2 etc... Atraves dessa 
aplicação todo esse processo se torna digital, sem o de custo de tinta e folha para imprimir e sem a necessidade de ''correr'' atras do 
assinante, podendo assim apenas notifica-lo que há uma requisição e o mesmo podendo assinar digitalmente e ainda salvar seu 
documento no próprio servidor da empresa(ou na máquina em esteja à rodar).

abaixo segue a descrição de umas definições, importações e de cada rota e seu funcionamento

<lu>
<li>Alguns imports basicos do ```Flask```, o ```mysql.connector``` para o banco de dados, ```win32``` para os disparos de emails e ```pythoncom``` para manter a conexão com o outlook<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242154640347298/image.png?width=960&height=129'>
<li>
Denifições padrões para o funcionamento (alterar os valores no ```mysql.connector.connect``` para o seu sistema)
```app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER``` é para podermos referenciar a pasta onde ficará salvo os arquivos assinados
```app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000``` tamanho máximo do arquivo a ser salvo<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242265785221161/image.png'>

<li>Esse é um sistema de autenticação simples padrão do Flask, apenas colei e copiei e fiz alterações<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242366020681758/image.png?width=631&height=468'>

<li>Sistema para sair do perfil<br>

<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242440545079346/image.png'>

<li>Aqui é a rota baixar fazer o upload do arquivo, duas rotas pois a primeira apenas mantem o nome do arquivo quando salvo e a segunda altera o nome do arquivo e uploads é a rota para poder assinar o arquivo<br>

<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242622116515890/image.png?width=639&height=468'>

<li>Sistemas de disparos de emails padrão do python <br>

<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242762294337637/image.png?width=590&height=468'>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242858834636851/image.png'>

<li>Um metodo para para exlcuir o pedido do banco de dados quando ele for aprovado, pois no fim ha um banco de dados que salva os finalizados<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081242948626301018/image.png'>

<li>Essa é uma routa exclusiva para excluir o pedido, não usei o anterior eu teria que saber exatamente qual o db e teria que acrescentar linhas de código com mais árvores de decisões desnecessárias<br>

<img src='https://media.discordapp.net/attachments/1050439862735609888/1081267379146850434/image.png?width=774&height=468'>

<li>Primeiro request para o fluxo cotação, a árvore de decisão é pois enviando dados do tipo NULL estava barrando o db, então eu envio apenas o valores verdadeiros e os setar os restantes como NULL<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081267628112355328/image.png?width=729&height=467'>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081267693258293249/image.png?width=960&height=271'>

<li>Isso daqui é padrão que segue várias vezes no código, pois a visualização no HTML é feita via JAVASCRIPT entao eu envio pra um endereço como jsonify e via JS, eu pego esse endereço e o personalizo monstrando em outro endereço<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081267750246301746/image.png?width=809&height=468'>

<li>Várias outras rotas seguem esse estilo abaixo, fazendo o POST pelo próprio python porem tambem há outras feitas pelo JAVASCRIPT<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081268313063166032/image.png?width=960&height=246'>

<li>Este é um exemplo, mas O POR QUE? bom era requisito automaticamente deixar em evidencia a cotação mais barata, isso é melhor visto no arquivo HTML, e como isso é feito pelo JS, o próprio POST é feito para esse endereço, e o mesmo finaliza o POST puxando os dados enviados do JS como json atraves do AXIOS<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081268532899221564/image.png?width=960&height=206'>

<li>Essa é uma rota que tambem era requisito. Voltar para o solicitante para atualizar dados e enviar para o financeiro. data_pgt tem essa repetição pois o db só estava aceitando o dados do tipo date em string e para ele entender que era uma string, eu envio a data dentro de aspas<br>
<img src='https://media.discordapp.net/attachments/1050439862735609888/1081268979160580156/image.png?width=960&height=414'>


Nos arquivos HTLMs os codigos JS são bem repetitivos e simples entao eu vou docuementar aqui o mais diferente deles


<strong>gestor.html</strong><br>
Aqui inicialmente eram 3 html que eu juntei em apenas 1. O primeiro GET que é de cotação, realiza o processo ja mencionado anteriormente que atraves de um input[type=radio], ele ja deixa selecionado o de menor valor. Porém isso causa muitos problemas como valores NULL considerarem 0 e cairem no check e pra melhorar a visualização, eu não queria mostrar os valores NULL nem como 0 então eu recorri a nubisse e criei um monte de árvore de decisão. De qualquer forma no fim, ele funcionou do jeito que eu queria mesmo afetando meu ego. Cada botão de aprovação e reprovação é intricamente ligado ao pedido em json, assim eu posso vincular o id ao botão e colocar para redicionar para um endereço que ira realizar o processo utilizando o id e retornando para a página anterior.
```
async function  getPedidos(){
    const response = await axios.get('http://127.0.0.1:5000/cotacao/pendencias/Pendencia')
    const pedidos = response.data
    const final = document.getElementById('final')
    const divAbs = document.createElement('div')
    divAbs.className='divAbs'

    pedidos.forEach(element => {
        const newDiv = document.createElement('div')
        newDiv.className = "divPedidos"

        final.appendChild(newDiv)

        const varNome = document.createElement('p')

        newDiv.appendChild(varNome)
        varNome.innerHTML=`
            <h3>ID: ${element.id}</h3>
            <h4>Tipo: Cotação</h4>
            <p>Nome: ${element.nome}</p>
            <p>Setor: ${element.setor}</p>
            <p>PA: ${element.PA}</p>
            <p>Motivo: ${element.motivo}</p>
        `
        if (element.valor3 != null && element.valor4 != null){
            if (element.valor1 < element.valor2 && element.valor1 < element.valor3 && element.valor1 < element.valor4){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" checked >
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                <input type="radio" name="group${element.id}" id="opt_4" >
                <label for="opt_4">Solicitação 4: ${element.solicitacao4} Valor 4: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

            }else if (element.valor2 < element.valor1 && element.valor2 < element.valor3 && element.valor2 < element.valor4){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" >
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" checked >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                <input type="radio" name="group${element.id}" id="opt_4" >
                <label for="opt_4">Solicitação 4: ${element.solicitacao4} Valor 4: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

            }else if (element.valor3 < element.valor1 && element.valor3 < element.valor2 && element.valor3 < element.valor4){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1">
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" checked >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                <input type="radio" name="group${element.id}" id="opt_4" >
                <label for="opt_4">Solicitação 4: ${element.solicitacao4} Valor 4: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

            }else{
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" >
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                <input type="radio" name="group${element.id}" id="opt_4" checked >
                <label for="opt_4">Solicitação 4: ${element.solicitacao4} Valor 4: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

        }}else if (element.valor4 != null && element.valor3 == null){
            if (element.valor1 < element.valor2 && element.valor1 < element.valor4){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" checked >
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao4} Valor 3: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

            }else if (element.valor2 < element.valor1 && element.valor2 < element.valor4){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" >
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" checked >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao4} Valor 3: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

            }else if (element.valor4 < element.valor1 && element.valor4 < element.valor2){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1">
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2">
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" checked>
                <label for="opt_3">Solicitação 3: ${element.solicitacao4} Valor 3: ${element.valor4}</label><br>
                `
                varNome.appendChild(a)

        }}else if (element.valor3 != null){
            if (element.valor1 < element.valor2 && element.valor1 < element.valor3){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" checked>
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                `
                varNome.appendChild(a)

            }else if (element.valor2 < element.valor1 && element.valor2 < element.valor3){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1">
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" checked >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                `
                varNome.appendChild(a)

            }else if (element.valor3 < element.valor1 && element.valor3 < element.valor2){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1">
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2">
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                <input type="radio" name="group${element.id}" id="opt_3" checked >
                <label for="opt_3">Solicitação 3: ${element.solicitacao3} Valor 3: ${element.valor3}</label><br>
                `
                varNome.appendChild(a)


        }}else if (element.valor4 == null && element.valor3 == null){
            if (element.valor1 < element.valor2){
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1" checked>
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                `
                varNome.appendChild(a)

            }else{
                const a = document.createElement('p')
                a.innerHTML=`
                <input type="radio" name="group${element.id}" id="opt_1">
                <label for="opt_1">Soliciatção 1: ${element.solicitacao1} Valor 1: ${element.valor1}</label><br>
                <input type="radio" name="group${element.id}" id="opt_2" checked >
                <label for="opt_2">Solicitação 2: ${element.solicitacao2} Valor 2: ${element.valor2}</label><br>
                `
                varNome.appendChild(a)
        }}
                const file = document.createElement('button')
                file.onclick=function(){window.open(`http://127.0.0.1:5000/uploads/Cotacao-${element.nome}.pdf`,'_blank')}
                file.innerText="Arquivo para Assinatura"
                file.className="buttonFile"
                newDiv.appendChild(file)

                const agree = document.createElement('button')
                agree.onclick=function(){alertinhaA("Aprovado")
                window.location.href=`http://127.0.0.1:5000/pedido/cotacao/aprovado/gestor/${element.id}`}
                agree.innerText="Aprovar"
                agree.className="buttonAprovar"
                newDiv.appendChild(agree)

                const dgree = document.createElement('button')
                dgree.onclick=function(){alertinhaR("Reprovado")
                window.location.href=`http://127.0.0.1:5000/pedido/cotacao/reprovado/Pendencia/${element.id}`}
                dgree.innerText="Reprovar"
                dgree.className='buttonReprovar'
                newDiv.appendChild(dgree)
    })
    const responseRem = await axios.get('http://127.0.0.1:5000/reembolso/pendencia/pendencias')
    const pedidosRem = responseRem.data

    pedidosRem.forEach(element => {

        const newDivRem = document.createElement('div')
        newDivRem.className = "divPedidos"

        final.appendChild(newDivRem)

        const varNomeRem = document.createElement('p')

        newDivRem.appendChild(varNomeRem)
        varNomeRem.innerHTML=`
            <h3>ID: ${element.id}</h3>
            <h4>Tipo: Reembolso</h4>
            <p>Nome: ${element.nome}</p>
            <p>Setor: ${element.setor}</p>
            <p>PA: ${element.PA}</p>
            <p>Motivo: ${element.motivo}</p>
            <p>Descrição: ${element.descricao}</p>
            <p>Destino: ${element.destino}</p>
            <p>Valor: ${element.valor}</p>
        `
                const fileRem = document.createElement('button')
                fileRem.onclick=function(){window.open(`http://127.0.0.1:5000/uploads/Reembolso-Nome-${element.nome}.pdf`,'_blank')}
                fileRem.innerText="Arquivo para Assinatura"
                fileRem.className="buttonFile"
                newDivRem.appendChild(fileRem)

                const agreeRem = document.createElement('button')
                agreeRem.onclick=function(){alertinhaA("Aprovado")
                window.location.href=`http://127.0.0.1:5000/pedido/reembolso/aprovado/pendencias/${element.id}`}
                agreeRem.innerText="Aprovar"
                agreeRem.className="buttonAprovar"
                newDivRem.appendChild(agreeRem)

                const dgreeRem = document.createElement('button')
                dgreeRem.onclick=function(){alertinhaR("Reprovado")
                window.location.href=`http://127.0.0.1:5000/pedido/reembolso/reprovado/pendencia/${element.id}`}
                dgreeRem.innerText="Reprovar"
                dgreeRem.className='buttonReprovar'
                newDivRem.appendChild(dgreeRem)
    })
    const responseSoli = await axios.get('http://127.0.0.1:5000/solicitacao/pendencias/Pendencia')
    const pedidosSoli = responseSoli.data

    pedidosSoli.forEach(element => {

        const newDivSoli = document.createElement('div')
        newDivSoli.className = "divPedidos"

        final.appendChild(newDivSoli)

        const varNomeSoli = document.createElement('p')

        newDivSoli.appendChild(varNomeSoli)

        varNomeSoli.innerHTML=`
            <h3>ID: ${element.id}</h3>
            <h4>Tipo: Solicitação</h4>
            <p>Nome: ${element.nome}</p>
            <p>Setor: ${element.setor}</p>
            <p>PA: ${element.PA}</p>
            <p>Motivo: ${element.motivo}</p>
            <p>Solicitação: ${element.solicitacao} Valor: ${element.valor}</p>
        `
                const fileSoli = document.createElement('button')
                fileSoli.onclick=function(){window.open(`http://127.0.0.1:5000/uploads/Solicitacao-${element.nome}.pdf`,'_blank')}
                fileSoli.innerText="Arquivo para Assinatura"
                fileSoli.className="buttonFile"
                newDivSoli.appendChild(fileSoli)

                const agreeSoli = document.createElement('button')
                agreeSoli.onclick=function(){alertinhaA("Aprovado")
                window.location.href=`http://127.0.0.1:5000/pedido/solicitacao/aprovado/gestor/${element.id}`}
                agreeSoli.innerText="Aprovar"
                agreeSoli.className="buttonAprovar"
                newDivSoli.appendChild(agreeSoli)

                const dgreeSoli = document.createElement('button')
                dgreeSoli.onclick=function(){alertinhaR("Reprovado")
                window.location.href=`http://127.0.0.1:5000/pedido/solicitacao/reprovado/Pendencia/${element.id}`}
                dgreeSoli.innerText="Reprovar"
                dgreeSoli.className='buttonReprovar'
                newDivSoli.appendChild(dgreeSoli)
    })
}


function alertinhaA(msg){
    const divMessage= document.querySelector('.alert');

    const message = document.createElement('div')
    message.className='messageA'
    message.innerText=msg
    divMessage.appendChild(message)

    setTimeout(()=>{
        message.style.display='none'},3000)
}
function alertinhaR(msg){
    const divMessage= document.querySelector('.alert');

    const message = document.createElement('div')
    message.className='messageR'
    message.innerText=msg
    divMessage.appendChild(message)

    setTimeout(()=>{
        message.style.display='none'},3000)
}
getPedidos()

```
