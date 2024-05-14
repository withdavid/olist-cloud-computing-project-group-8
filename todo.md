## OLIST CLOUD PROJECT

### Fase 1: Definição do Conjunto de Dados e Capacidades de Negócio
- **Tarefa:** Selecionar um conjunto de dados que atenda aos critérios especificados e definir as capacidades de negócio.
- **Entregáveis:**
  - [x] Tema e resumo do conjunto de dados.
  - [x] Lista das capacidades de negócio identificadas.
  - [x] Detalhes do conjunto de dados: data de criação/atualização, tipo de arquivo, tamanho e link.

### Fase 2: Especificação do Sistema
- **Tarefa:** Definir casos de uso, especificar a API REST e criar um design arquitetônico preliminar.
- **Entregáveis:**
  - [x] Diagramas de casos de uso.
  - [x] Especificação da API REST (YAML/JSON).
  - [x] Diagrama e descrição da arquitetura da aplicação.

### Fase 3: Implementação
- **Tarefa:** Preparar o repositório, implementar a aplicação, containerizar os microsserviços e automatizar a construção/deploy.
- **Entregáveis:**
  - [x] Arquivo zip com o código-fonte do projeto, scripts, configurações, arquitetura técnica.
  - [x] Release "Fase3" e comando git clone.

Claro, aqui estão os entregáveis para a Fase 4, com checkboxes:

### Fase 4: Deploy
- **Tarefa:** Fazer o deploy dos containers em um cluster Kubernetes na nuvem (GKE).
- **Entregáveis:**
  - [ ] Containers implantados com sucesso no cluster Kubernetes.
  - [ ] Certificar-se de que os arquivos de banco de dados com os conjuntos de dados estejam localizados em um volume Kubernetes.
  - [ ] Usar um ingress HTTP(s) para conectar cada microsserviço frontend ao balanceador de carga na nuvem.
  - [ ] Configurar política de escalabilidade Kubernetes (HPA e, se necessário, VPA e Cluster).
  - [ ] Expor apenas os serviços que realmente precisam ser acessados externamente.
  - [ ] Implementar autenticação e autorização para diferenciar os endpoints da API (premium requer autenticação).
  - [ ] Configurar utilização de recursos através de pedidos e limites para otimização de custos.
  - [ ] Configurar métricas por pod para monitoramento com Prometheus.
  - [ ] Configurar sondas personalizadas para liveness, readiness e startup.
  - [ ] Implementar atualizações e rollback automáticos.

### Fase 7: Revisão
- **Tarefa:** Propor melhorias relacionadas à nuvem e preparar um plano para a implementação e deploy finais.
- **Entregáveis:** Documento PDF com seções do plano adaptadas ao foco do grupo.
- [x] PDF de melhorias.

### Fase 8: Implementação e Deploy
- **Tarefa:** Implementar e fazer o deploy das novas contribuições.
- **Entregáveis:** Arquivo ZIP com as novas contribuições.
- [ ] Novas contribuições

### Fase 9: Testes e Avaliação
- **Tarefa:** Testar e avaliar a aplicação em suporte operacional, segurança, confiabilidade, eficiência de desempenho, otimização de custos e observabilidade.
- **Entregáveis:** Documento PDF com resultados dos testes e avaliação de custos.
- [ ] Testes de stress.

### Fase 10: Relatório Final
- **Tarefa:** Documentar o projeto completo, incluindo motivação, casos de uso, arquitetura, implementação, deploy, resultados dos testes e conclusões.
- **Entregáveis:** Documento PDF com relatório final abrangente.
- [ ] PDF relatório final.