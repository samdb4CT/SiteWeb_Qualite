<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <se:Name>pf001_finessgeocode_mlyon_2154</se:Name>
    <UserStyle>
      <se:Name>pf001_finessgeocode_mlyon_2154</se:Name>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>Centres Hospitaliers</se:Name>
          <se:Description>
            <se:Title>Centres Hospitaliers</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:Or>
                  <ogc:Or>
                    <ogc:Or>
                      <ogc:PropertyIsEqualTo>
                        <ogc:PropertyName>type</ogc:PropertyName>
                        <ogc:Literal>Centres Hospitaliers</ogc:Literal>
                      </ogc:PropertyIsEqualTo>
                      <ogc:PropertyIsEqualTo>
                        <ogc:PropertyName>type</ogc:PropertyName>
                        <ogc:Literal>Centres Hospitaliers Régionaux</ogc:Literal>
                      </ogc:PropertyIsEqualTo>
                    </ogc:Or>
                    <ogc:PropertyIsEqualTo>
                      <ogc:PropertyName>type</ogc:PropertyName>
                      <ogc:Literal>Centres Hospitaliers Spécialisés Lutte Maladies Mentales</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:Or>
                  <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>type</ogc:PropertyName>
                    <ogc:Literal>Centres de Lutte contre le Cancer</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:Or>
                <ogc:PropertyIsEqualTo>
                  <ogc:PropertyName>type</ogc:PropertyName>
                  <ogc:Literal>Dialyse Ambulatoire</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:Or>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>type</ogc:PropertyName>
                <ogc:Literal>Hôpitaux Locaux</ogc:Literal>
              </ogc:PropertyIsEqualTo>
            </ogc:Or>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:Mark>
                <se:WellKnownName>circle</se:WellKnownName>
                <se:Fill>
                  <se:SvgParameter name="fill">#a3eb81</se:SvgParameter>
                </se:Fill>
                <se:Stroke>
                  <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                </se:Stroke>
              </se:Mark>
              <se:Size>21</se:Size>
            </se:Graphic>
          </se:PointSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>EPHAD &amp; maison de retraites</se:Name>
          <se:Description>
            <se:Title>EPHAD &amp; maison de retraites</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>type</ogc:PropertyName>
              <ogc:Literal>Etablissements d'Hébergement pour Personnes âgées</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:Mark>
                <se:WellKnownName>circle</se:WellKnownName>
                <se:Fill>
                  <se:SvgParameter name="fill">#19d75f</se:SvgParameter>
                </se:Fill>
                <se:Stroke>
                  <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                </se:Stroke>
              </se:Mark>
              <se:Size>14</se:Size>
            </se:Graphic>
          </se:PointSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Autres établissements de santé</se:Name>
          <se:Description>
            <se:Title>Autres établissements de santé</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:And>
                <ogc:And>
                  <ogc:And>
                    <ogc:And>
                      <ogc:And>
                        <ogc:And>
                          <ogc:PropertyIsNotEqualTo>
                            <ogc:PropertyName>type</ogc:PropertyName>
                            <ogc:Literal>Centres Hospitaliers</ogc:Literal>
                          </ogc:PropertyIsNotEqualTo>
                          <ogc:PropertyIsNotEqualTo>
                            <ogc:PropertyName>type</ogc:PropertyName>
                            <ogc:Literal>Centres Hospitaliers Régionaux</ogc:Literal>
                          </ogc:PropertyIsNotEqualTo>
                        </ogc:And>
                        <ogc:PropertyIsNotEqualTo>
                          <ogc:PropertyName>type</ogc:PropertyName>
                          <ogc:Literal>Centres Hospitaliers Spécialisés Lutte Maladies Mentales</ogc:Literal>
                        </ogc:PropertyIsNotEqualTo>
                      </ogc:And>
                      <ogc:PropertyIsNotEqualTo>
                        <ogc:PropertyName>type</ogc:PropertyName>
                        <ogc:Literal>Centres de Lutte contre le Cancer</ogc:Literal>
                      </ogc:PropertyIsNotEqualTo>
                    </ogc:And>
                    <ogc:PropertyIsNotEqualTo>
                      <ogc:PropertyName>type</ogc:PropertyName>
                      <ogc:Literal>Dialyse Ambulatoire</ogc:Literal>
                    </ogc:PropertyIsNotEqualTo>
                  </ogc:And>
                  <ogc:PropertyIsNotEqualTo>
                    <ogc:PropertyName>type</ogc:PropertyName>
                    <ogc:Literal>Hôpitaux Locaux</ogc:Literal>
                  </ogc:PropertyIsNotEqualTo>
                </ogc:And>
                <ogc:PropertyIsNotEqualTo>
                  <ogc:PropertyName>type</ogc:PropertyName>
                  <ogc:Literal>Etablissements d'Hébergement pour Personnes âgées</ogc:Literal>
                </ogc:PropertyIsNotEqualTo>
              </ogc:And>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>type</ogc:PropertyName>
                <ogc:Literal>Logements en Structure Collective</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:Mark>
                <se:WellKnownName>circle</se:WellKnownName>
                <se:Fill>
                  <se:SvgParameter name="fill">#b3585c</se:SvgParameter>
                </se:Fill>
                <se:Stroke>
                  <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                </se:Stroke>
              </se:Mark>
              <se:Size>11</se:Size>
            </se:Graphic>
          </se:PointSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Logements en Structure Collective</se:Name>
          <se:Description>
            <se:Title>Logements en Structure Collective</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>type</ogc:PropertyName>
              <ogc:Literal>Logements en Structure Collective</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:Mark>
                <se:WellKnownName>circle</se:WellKnownName>
                <se:Fill>
                  <se:SvgParameter name="fill">#2dc9b2</se:SvgParameter>
                </se:Fill>
                <se:Stroke>
                  <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                </se:Stroke>
              </se:Mark>
              <se:Size>7</se:Size>
            </se:Graphic>
          </se:PointSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
